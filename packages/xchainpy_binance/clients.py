from binance_chain.http import AsyncHttpApiClient
from binance_chain.constants import KlineInterval
from binance_chain.environment import BinanceEnvironment
from binance_chain.messages import TransferMsg
from binance_chain.wallet import Wallet

from xchainpy_client import interface
from xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy_binance import crypto
from xchainpy_binance import utils
from xchainpy_util.asset import Asset

class Client(interface.IXChainClient): # create an interface for binance methods (getprivate_key, get_client_url and ...)

    phrase = address = network = ''
    private_key = client = None

    def __init__(self, phrase, network = 'testnet'):
        self.set_network(network)
        self.set_phrase(phrase)

    def get_client_url(self):
        """Get client url
        :returns: the client url for binance chain based on the network
        """
        return 'https://testnet-dex.binance.org' if self.network == 'testnet' else 'https://dex.binance.org'

    def get_private_key(self):
        """Get private key

        :returns: the private key generated from the given phrase
        :raises: raise an exception if phrase not set
        """
        if not self.private_key:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.private_key = crypto.mnemonic_to_private_key(self.phrase) # passPhrase ?
        return self.private_key

    def get_address(self):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if not self.address:
            self.address = crypto.private_key_to_address(self.get_private_key(), utils.get_prefix(self.network))
            if not self.address :
                raise Exception("Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key.")
        return self.address


    def set_phrase(self, phrase: str):
        """Set/Update a new phrase

        :param phrase: A new phrase
        :type phrase: str
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """
        
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")    
            
            self.phrase = phrase
            self.private_key = None
            self.address = ''

        return self.get_address()

    def set_network(self, network: str):
        """Set/update the current network

        :param network: "mainnet" or "testnet"
        :type network: str
        :returns: the client
        :raises: raises if network not provided
        :raises: `Invalid network' if the given network is invalid
        """
        if not network:
            raise Exception("Network must be provided")
        else:
            self.network = network
            # choose network (testnet or mainnet)
            if self.network == 'testnet':
                # initialise with Testnet environment
                testnet_env = BinanceEnvironment.get_testnet_env()
                self.client = AsyncHttpApiClient(env=testnet_env)
            elif self.network == 'mainnet':
                # Alternatively pass no env to get production
                self.client = AsyncHttpApiClient()
            else: 
                raise Exception("Invalid network")
        self.address = ''
        return self.client

    def get_network(self):
        """Get the current network
        :returns: the current network. (`mainnet` or `testnet`)
        """
        return self.network

    def get_balance(self, address: str, asset):
        pass

    def transfer(self, asset : Asset , amount , recipient , memo=''):
        """transfer balances

        :param asset: asset object containing : chain , symbol , ticker(optional)
        :type asset: Asset
        :param amount: amount of asset to transfer (don't multiply by 10**8)
        :type amount: int , float , decimal
        :param recipient: destination address
        :type recipient: str
        :param memo: optional memo for transaction
        :type memo: str
        :returns: result of transfer
        :raises: raises if asset or amount or destination address not provided
        """
        wallet = Wallet(self.get_private_key())
        client = AsyncHttpApiClient()

        if not asset:
            raise Exception('Asset must be provided')
        if not amount:
            raise Exception('Amount must be provided')
        if not recipient:
            raise Exception('Destination address must be provided')

        transfer_msg = TransferMsg(
            wallet=wallet,
            symbol=asset.symbol,
            amount=amount,
            to_address=recipient,
            memo=memo
        )
        res = client.broadcast_msg(transfer_msg, sync=True) # sync mode
        return res

    def get_fees(self):
        pass