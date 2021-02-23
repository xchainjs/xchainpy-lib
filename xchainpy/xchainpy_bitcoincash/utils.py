import datetime

import bitcash
from xchainpy.xchainpy_bitcoincash.models.api_types import Transaction
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

def calc_fee(fee_rate , memo = None , utxos = None):
    key = bitcash.PrivateKey()
    random_address = key.address
    transaction = key.create_transaction(utxos or [(random_address,0,'bch')],fee=fee_rate,message=memo)
    # to be continued
    