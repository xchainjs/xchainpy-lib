from binance_chain.http import AsyncHttpApiClient
from binance_chain.constants import KlineInterval
from binance_chain.environment import BinanceEnvironment

from xchainpy_client import interface
from xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy_binance import crypto
from xchainpy_binance import utils

class Client(interface.IXChainClient): # create an interface for binance methods (getprivatekey, getClientUrl and ...)

    phrase = address = network = ''
    privateKey = client = None

    def __init__(self, phrase, network = 'testnet'):
        self.setNetwork(network)
        self.setPhrase(phrase)

    def getClientUrl(self):
        return 'https://testnet-dex.binance.org' if self.network == 'testnet' else 'https://dex.binance.org'

    def getPrivateKey(self):
        """Get private key
        :returns: the private key generated from the given phrase
        :raises: raise an exception if phrase not set
        """
        if not self.privateKey:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.privateKey = crypto.mnemonicToPrivateKey(self.phrase) # passPhrase ?
        return self.privateKey

    def getAddress(self):
        """Get the current address
        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if not self.address:
            self.address = crypto.privateKeyToAddress(self.getPrivateKey(), utils.getPrefix(self.network))
            if not self.address :
                raise Exception("Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key.")
        return self.address


    def setPhrase(self, phrase: str):
        """Set/Update a new phrase
        :param phrase: A new phrase
        :type phrase: str
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """
        
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validatePhrase(phrase):
                raise Exception("invalid phrase")    
            
            self.phrase = phrase
            self.privateKey = None
            self.address = ''

        return self.getAddress()

    def setNetwork(self, network: str):
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
        return self.client

    def getBalance(self, address: str, asset):
        pass

    def transfer(self, txParams):
        pass

    def getFees(self):
        pass
