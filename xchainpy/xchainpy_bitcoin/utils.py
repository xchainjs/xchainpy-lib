from bitcoinlib.keys import Address
from typing import List, Optional, Union
import asyncio
from xchainpy.xchainpy_bitcoin.const import MIN_TX_FEE
from xchainpy.xchainpy_bitcoin.models.common import DerivePath, UTXO
from bitcoinlib.services.services import *
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models.balance import Balance
from xchainpy.xchainpy_util.chain import BTCCHAIN
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_bitcoin import sochain_api
import datetime
import binascii


TX_EMPTY_SIZE = 4 + 1 + 1 + 4  # 10
TX_INPUT_BASE = 32 + 4 + 1 + 4  # 41
TX_INPUT_PUBKEYHASH = 107
TX_OUTPUT_BASE = 8 + 1  # 9
TX_OUTPUT_PUBKEYHASH = 25
DUST_THRESHOLD = 1000


def get_derive_path(index: int = 0):
    return DerivePath(index=index)


def parse_tx(tx):
    """Parse tx

    :param tx: The transaction to be parsed
    :type tx: str
    :returns: The transaction parsed from the binance tx
    """
    asset = Asset.from_str(f'{BTCCHAIN}.BTC')
    tx_from = [tx_types.TxFrom(i['address'], i['value']) for i in tx['inputs']]
    tx_to = [tx_types.TxTo(i['address'], i['value']) for i in tx['outputs']]
    tx_date = datetime.datetime.fromtimestamp(tx['time'])
    tx_type = 'transfer'
    tx_hash = tx['txid']

    tx = tx_types.TX(asset, tx_from, tx_to, tx_date, tx_type, tx_hash)
    return tx


def calc_fee(fee_rate, memo=''):
    """Calculate fees based on fee rate and memo

    :param fee_rate: fee rate
    :type fee_rate: int
    :param memo: memo
    :type memo: str
    :returns: The calculated fees based on fee rate and the memo
    """
    compiled_memo = compile_memo(memo) if memo else None
    fee = get_fee([], fee_rate, compiled_memo)
    return fee


def compile_memo(memo: str):
    """Compile memo

    :param memo: The memo to be compiled
    :type memo: str
    :returns: The compiled memo
    """
    metadata = bytes(memo, 'utf-8')
    metadata_len = len(metadata)

    if metadata_len <= 75:
        # length byte + data (https://en.bitcoin.it/wiki/Script)
        payload = bytearray((metadata_len,))+metadata
    elif metadata_len <= 256:
        # OP_PUSHDATA1 format
        payload = "\x4c"+bytearray((metadata_len,))+metadata
    else:
        payload = "\x4d"+bytearray((metadata_len % 256,))+bytearray(
            (int(metadata_len/256),))+metadata  # OP_PUSHDATA2 format
    

    compiled_memo = binascii.b2a_hex(payload).decode('utf-8')
    compiled_memo = '6a' + compiled_memo
    compiled_memo = binascii.unhexlify(compiled_memo)
    return compiled_memo


def validate_address(network, address):
    """Validate the BTC address

    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: True or False
    """
    try:
        address = Address.import_address(address=address, network=(
            'bitcoin' if network == 'mainnet' else network))
        return True
    except:
        return False


def get_fee(inputs: List[UTXO], fee_rate: float, data: Optional[bytes]=None):
    """Get the transaction fee

    :param inputs: the UTXOs
    :type inputs: List[UTXO]
    :param fee_rate: the fee rate
    :type fee_rate: float
    :param data: The compiled memo (Optional)
    :type data: bytes
    :returns: The fee amount
    """
    lst_reduce = 0
    if len(inputs) > 0:
        for x in inputs:
            lst_reduce += TX_INPUT_BASE + \
                (len(x.witness_utxo.script)
                 if x.witness_utxo.script else TX_INPUT_PUBKEYHASH)

    sum = TX_EMPTY_SIZE + lst_reduce + \
        len(inputs) + TX_OUTPUT_BASE + TX_OUTPUT_PUBKEYHASH + \
        TX_OUTPUT_BASE + TX_OUTPUT_PUBKEYHASH
    if data:
        sum = sum + TX_OUTPUT_BASE + len(data)
    fee = sum * fee_rate
    result = fee if fee > MIN_TX_FEE else MIN_TX_FEE
    return result


async def scan_UTXOs(network, address):
    """Scan UTXOs from sochain

    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: The UTXOs of the given address
    """
    utxos = await sochain_api.get_unspent_txs(network, address)
    utxos = list(map(UTXO.from_sochain_utxo, utxos))
    return utxos


async def get_change(value_out, network, address):
    """Get the balance changes amount

    :param value_out: amount you wnat to transfer
    :type value_out: int
    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: The UTXOs of the given address
    """
    try:
        balance = await sochain_api.get_balance(network, address)
        balance = balance * 10 ** 8
        change = 0
        if balance - value_out > DUST_THRESHOLD:
            change = balance - value_out
        return change
    except Exception as err:
        raise Exception(str(err))


async def build_tx(amount, recipient, memo, fee_rate, sender, network):
    """Build transcation

    :param amount: amount of BTC to transfer
    :type amount: int
    :param recipient: destination address
    :type recipient: str
    :param memo: optional memo for transaction
    :type memo: str
    :param fee_rate: fee rates for transaction
    :type fee_rate: int
    :param sender: sender's address
    :type sender: str
    :param network: testnet or mainnet
    :type network: str
    :returns: transaction
    """
    try:
        utxos = await scan_UTXOs(network, sender)
        if len(utxos) == 0:
            raise Exception("No utxos to send")

        balance = await sochain_api.get_balance(network, sender)

        if not validate_address(network, recipient):
            raise Exception('Invalid address')

        fee_rate_whole = int(fee_rate)

        compiled_memo = None
        if memo:
            compiled_memo = compile_memo(memo)

        fee = get_fee(utxos, fee_rate_whole, compiled_memo)

        if fee + amount > balance * 10 ** 8:
            raise Exception('Balance insufficient for transaction')

        t = Transaction(network=network, witness_type='segwit')

        for i in utxos:
            t.add_input(prev_txid=i.hash, output_n=i.index,
                    value=i.witness_utxo.value, witnesses=i.witness_utxo.script)

        t.add_output(address=recipient, value=amount)
        change = await get_change(amount + fee, network, sender)
        
        if change > 0:
            t.add_output(address=sender, value=int(change))

        if compiled_memo:
            t.add_output(lock_script=compiled_memo, value=0)

        return t, utxos

    except Exception as err:
        raise Exception(str(err))


async def broadcast_tx(network, tx_hex):
    """Broadcast the transaction

    :param network: testnet or mainnet
    :type network: str
    :param tx_hex: tranaction hex
    :type tx_hex: str
    :returns: The transaction hash
    """
    return await sochain_api.broadcast_tx(network, tx_hex)
