from bitcoinlib.keys import Address
import binascii
from typing import List, Optional, Union

from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_litecoin.models.common import DerivePath, UTXO


TX_EMPTY_SIZE = 4 + 1 + 1 + 4  # 10
TX_INPUT_BASE = 32 + 4 + 1 + 4  # 41
TX_INPUT_PUBKEYHASH = 107
TX_OUTPUT_BASE = 8 + 1  # 9
TX_OUTPUT_PUBKEYHASH = 25
DUST_THRESHOLD = 1000

MIN_TX_FEE = 1000

def get_derive_path(index:int=0):
    return DerivePath(index=index)

def validate_address(network, address):
    """Validate the LTC address

    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: True or False
    """
    try:
        address = Address.import_address(address=address, network=(
            'litecoin' if network == 'mainnet' else 'litecoin_testnet'))
        return True
    except:
        return False

def network_to_bitcoinlib_format(network: str):
    return 'litecoin' if network == 'mainnet' else 'litecoin_testnet'


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