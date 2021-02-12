
from xchainpy.xchainpy_crypto.crypto import validate_phrase
from xchainpy.xchainpy_client.interface import IXChainClient
from xchainpy.xchainpy_bitcoin import utils

from bitcoinlib.wallets import Wallet
from bitcoinlib.wallets import *
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_bitcoin import sochain_api
from xchainpy.xchainpy_client.models.balance import Balance
from xchainpy.xchainpy_util.asset import Asset


class IBitcoinClient():
    def derive_path(self):
        pass
    def get_fees_with_rates(self):
        pass
    def get_fees_with_memo(self): 
        pass
    def get_fee_rates(self): 
        pass

class Client(IBitcoinClient,IXChainClient):

    node_url = node_api_key = phrase = net = address = ''
    wallet = None

    def __init__(self, phrase , network='testnet'):
        self.set_network(network)
        self.set_phrase(phrase)
        self.service = Service(network=self.get_network())


    def set_network(self, network: str):
        if not network :
            raise Exception("Network must be provided")
        else:
            if not network in ['testnet' , 'mainnet']:
                raise Exception('Invalid network')
            else:
                self.net = network
    
    def set_wallet(self, phrase):
        # self.wallet = Wallet("Wallet")
        wallet_delete_if_exists('Wallet')
        self.wallet = Wallet.create("Wallet", keys=self.phrase , witness_type='segwit', network=self.get_network())
        return self.wallet

    def set_phrase(self , phrase : str):
        if validate_phrase(phrase):
            self.phrase = phrase
            self.set_wallet(self.phrase)
            address = self.get_address()
            return address
        else:
            raise Exception("Invalid Phrase")


    def purge_client(self):
        """Purge client
        """
        self.phrase = ''

    def get_network(self):
        """Get the current network
        :returns: the current network. (`mainnet` or `testnet`)
        """
        return self.net if self.net == 'testnet' else 'bitcoin'

    def derive_path(self):
        return utils.get_derive_path().testnet if self.net == 'testnet' else utils.get_derive_path().mainnet


    def get_address(self):
        """Get private key

        :returns: the private key generated from the given phrase
        :raises: raise an exception if phrase not set
        """
        if self.phrase:
            self.address = self.wallet.get_key().address
        
            if not self.address:
                raise Exception('Address not defined')

            return self.address
        raise Exception('Phrase must be provided')

    async def get_balance(self, address:str=None):
        try:
            amount = await utils.get_balance(self.service, address or self.address)
            amount = round(amount * 10 ** -8, 8) 
            balance = Balance(Asset.from_str('BTC.BTC'), amount)
            return balance
        except Exception as err:
            raise Exception(str(err))

    async def get_transactions(self, params: tx_types.TxHistoryParams):
        try:
            transactions = await sochain_api.get_transactions(self.net, self.address)
            total = transactions['total_txs']
            txs = []
            for tx in transactions['txs']:
                tx = await sochain_api.get_tx(self.net, tx['txid'])
                tx = utils.parse_tx(tx)
                txs.append(tx)

            return {
                'total': total,
                'tx': txs
            }
        except Exception as err:
            raise Exception(str(err))


    async def get_transaction_data(self, tx_id:str):
        try:
            tx = await sochain_api.get_tx(self.net, tx_id)
            tx = utils.parse_tx(tx)
            return tx
        except Exception as err:
            raise Exception(str(err))


    async def get_fees_with_rates(self):
        tx_fee = await sochain_api.get_suggested_tx_fee()
        return {
                'rates': {
                    'fast': tx_fee * 5,
                    'fastest': tx_fee * 1,
                    'average': tx_fee * 0.5
                },
                'multi': {
                    'fast': tx_fee,
                    'fastest': tx_fee,
                    'average': tx_fee
                }
            }
