import datetime
from xchainpy_bitcoincash.models.api_types import TxUnspent
from cashaddress import convert
from bitcash import transaction
from xchainpy_util.asset import AssetBCH
from xchainpy_client.models.balance import Balance
from xchainpy_client.models import tx_types
from . import haskoin_api, bitcore_api



BCH_DECIMAL = 8
DEFAULT_SUGGESTED_TRANSACTION_FEE = 1

def parse_tx(tx):
    """Parse tx
    :param tx: The transaction to be parsed
    :type tx: str
    :returns: The transaction parsed from the binance tx
    """
    asset = AssetBCH
    tx_from = [tx_types.TxFrom(i['address'], i['value'] * 10 ** -8) for i in tx['inputs']]
    tx_to = [tx_types.TxTo(i['address'], i['value'] * 10 ** -8) for i in tx['outputs']]
    tx_date = datetime.datetime.fromtimestamp(tx['time'])
    tx_type = 'transfer'
    tx_hash = tx['txid']

    tx = tx_types.TX(asset, tx_from, tx_to, tx_date, tx_type, tx_hash)
    return tx

async def get_balance(haskoin_url:str, network:str, address:str):
    """Get the BCH balance of a given address

    :param haskoin_url: haskoin url
    :type haskoin_url: str
    :param address: BCH address
    :type address: str
    :param network: mainnet or testnet
    :type network: str
    :returns: The BCH balance of the address
    """
    try:
        account = await haskoin_api.get_account(haskoin_url, network, address)
        if not account:
                raise Exception("Invalid Address")
        
        balance = [Balance(AssetBCH, (account.confirmed + account.unconfirmed) * 10 ** -8)]
        return balance
    except Exception as err:
        raise Exception(str(err))

def calc_fee(fee_rate, memo=None, utxos=None):
    """Calculate fees based on fee rate and memo

    :param fee_rate: fee rates
    :type fee_rate: str
    :param memo: memo (optional)
    :type memo: str
    :param utxos: A list of utxos (optional)
    :type utxos: str
    :returns: The calculated fees based on fee rate and the memo
    """
    # key = PrivateKey()
    # random_address = key.address

    if utxos:
        utxos_len = len(utxos)
    else:
        utxos_len = 0

    # outputs = [(random_address, 0, 'bch')]
    # for i, output in enumerate(outputs):
    #     dest, amount, currency = output
    #     outputs[i] = (dest, transaction.currency_to_satoshi_cached(amount, currency))
    # num_outputs = len(outputs) + 1
    num_outputs = 2

    total_op_return_size = 0
    if memo:
        message_chunks = transaction.chunk_data(memo, transaction.MESSAGE_LIMIT)
        for message in message_chunks:
            total_op_return_size += transaction.get_op_return_size(message, custom_pushdata=False)

    calculated_fee = transaction.estimate_tx_fee(utxos_len, num_outputs, fee_rate, False, total_op_return_size)
    return calculated_fee

async def scan_UTXOs(haskoin_url, network, address):
    """Scan UTXOs from sochain

    :param haskoin_url: haskoin url
    :type haskoin_url: str
    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: The UTXOs of the given address
    """
    unspents = await haskoin_api.get_unspent_transactions(haskoin_url, network, address)
    utxos = list(map(TxUnspent.bitcash_unspent_from_object, unspents))
    return utxos

def validate_address(address):
    return convert.is_valid(address)

async def build_tx(haskoin_url, amount, recipient, memo, fee_rate, sender, network, key):
    """Build transcation

    :param haskoin_url: haskoin url
    :type haskoin_url: str
    :param amount: amount of BCH to transfer
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
    :param client_url: The haskoin API url
    :type client_url: str
    :param key: bitcash object
    :type key: object
    :returns: transaction
    """
    try:
        if not validate_address(recipient):
            raise Exception('Invalid address')

        utxos = await scan_UTXOs(haskoin_url, network, sender)
        if len(utxos) == 0:
            raise Exception("No utxos to send")

        balance = await get_balance(haskoin_url, network, sender)

        if not balance:
            raise Exception("No BCH balance found")

        outputs = [(recipient, amount, 'bch')]

        tx = key.create_transaction(outputs=outputs, fee=int(fee_rate), message=memo, unspents=utxos, leftover=sender)
        return tx

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
    return await bitcore_api.broadcast_tx(network, tx_hex)