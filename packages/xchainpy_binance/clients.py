from binance_chain.http import AsyncHttpApiClient
from binance_chain.constants import KlineInterval
from binance_chain.environment import BinanceEnvironment

from xchainpy_client import interface
from xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy_binance import crypto
from xchainpy_binance import utils

class Client(interface.IXChainClient): # create an interface for binance methods (getprivatekey, getClientUrl and ...)

    #add these params:
        # self.privateKey, self.privateKey, self.address, self.client
    phrase = address = network = ''
    privateKey = client = None

    def init(self, phrase, network = 'testnet'):
        self.setPhrase(phrase)
        self.setNetwork(phrase)

    def getClientUrl(self):
        return 'https://testnet-dex.binance.org' if self.network == 'testnet' else 'https://dex.binance.org'

    def getPrivateKey(self):
        if not self.privateKey:
            if not self.phrase:
                # thorw an err
                pass

            self.privateKey = crypto.mnemonicToPrivateKey(self.phrase) # passPhrase ?
        return self.privateKey

    def getAddress(self):
        if not self.address:
            self.address = crypto.privateKeyToAddress(self.getPrivateKey(), utils.getPrefix(self.network))
        return self.address


    def setPhrase(self, phrase: str):
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validatePhrase(phrase):
                pass # throw an err
            self.phrase = phrase
            self.privateKey = None
            self.address = ''

        return self.getAddress()

    def setNetwork(self, network: str):
        if not self.network and not self.client:
            # choose network (testnet or mainnet)
            if self.network == 'testnet':
                # initialise with Testnet environment
                testnet_env = BinanceEnvironment.get_testnet_env()
                self.client = AsyncHttpApiClient(env=testnet_env)
            elif self.network == 'mainnet':
                # Alternatively pass no env to get production
                self.client = AsyncHttpApiClient()
            else: 
                #thorw err
                pass
        return self.client

    def getBalance(self, address: str, asset):
        pass

    def transfer(self, txParams):
        pass

    def getFees(self):
        pass

    