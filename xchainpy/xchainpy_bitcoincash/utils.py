import datetime
import bitcash

from cashaddress import convert
from xchainpy.xchainpy_bitcoincash import haskoin_api

from bitcash import transaction, PrivateKey, PrivateKeyTestnet
from xchainpy.xchainpy_bitcoincash.models.api_types import Transaction, TxUnspent
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_util.chain import BITCOINCASH
from xchainpy.xchainpy_client.models import tx_types


BCH_DECIMAL = 8
DEFAULT_SUGGESTED_TRANSACTION_FEE = 1

class DerivePath:
    def __init__(self, index:int=0):

        self._mainnet = f"m/44'/145'/0'/0/{index}"
        self._testnet = f"m/44'/1'/0'/0/{index}"

    @property
    def mainnet(self):
        return self._mainnet

    @mainnet.setter
    def mainnet(self, mainnet):
        self._mainnet = mainnet

    @property
    def testnet(self):
        return self._testnet

    @testnet.setter
    def testnet(self, testnet):
        self._testnet = testnet

def get_derive_path(index: int = 0):
    return DerivePath(index=index)


class ClientUrl:
    def __init__(self , testnet , mainnet):
        self._testnet : str = testnet
        self._mainnet : str = mainnet

    @property
    def mainnet(self):
        return self._mainnet

    @mainnet.setter
    def mainnet(self, mainnet : str):
        self._mainnet = mainnet

    @property
    def testnet(self):
        return self._testnet

    @testnet.setter
    def testnet(self, testnet : str):
        self._testnet = testnet
    

def parse_tx(tx : Transaction):
    """Parse tx
    :param tx: The transaction to be parsed
    :type tx: str
    :returns: The transaction parsed from the binance tx
    """
    asset = Asset.from_str(f'{BITCOINCASH}.BCH')
    tx_from = [tx_types.TxFrom(i.address, i.value * 10 ** -8) for i in tx.inputs]
    tx_to = [tx_types.TxTo(i.address, i.value * 10 ** -8) for i in tx.outputs]
    tx_date = datetime.datetime.fromtimestamp(tx.time)
    tx_type = 'transfer'
    tx_hash = tx.txid

    tx = tx_types.TX(asset, tx_from, tx_to, tx_date, tx_type, tx_hash)
    return tx

def calc_fee(fee_rate , memo=None , utxos=None):
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

async def scan_UTXOs(client_url, address):
    """Scan UTXOs from sochain

    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: The UTXOs of the given address
    """
    unspents = await haskoin_api.get_unspent_transactions(client_url, address)
    utxos = list(map(TxUnspent.unspent_from_object, unspents))
    return utxos

def validate_address(address):
    return convert.is_valid(address)

async def build_tx(amount, recipient, memo, fee_rate, sender, network , client_url, key):
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
    :param client_url: The haskoin API url
    :type client_url: str
    :param key: bitcash object
    :type key: object
    :returns: transaction
    """
    try:
        utxos = await scan_UTXOs(client_url, sender)
        if len(utxos) == 0:
            raise Exception("No utxos to send")

        balance = (await haskoin_api.get_account(client_url , sender)).confirmed

        if not balance:
            raise Exception("No BCH balance found")

        if not validate_address(recipient):
            raise Exception('Invalid address')

        outputs = [(recipient, amount, 'bch')]

        tx = key.create_transaction(outputs=outputs, fee=int(fee_rate), message=memo, unspents=key.get_unspents(), leftover=sender)
        return tx

    except Exception as err:
        raise Exception(str(err))