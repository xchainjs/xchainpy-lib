from binance_chain.http import AsyncHttpApiClient
from binance_chain.constants import KlineInterval
from binance_chain.environment import BinanceEnvironment

from xchainpy_client import interface
from xchainpy_crypto import crypto

class Client(interface.IXChainClient):
    def init(self, phrase, network = 'testnet'):
        self.phrase = phrase
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
            #thorw err
            pass

        #set phrase ():
            # check phrase validity (xchainpy_crypto)

    def setPhrase(self, phrase: str):
        if not self.phrase or self.phrase != phrase:
            if not crypto.validatePhrase(phrase):
                pass # throw an err
            self.phrase = phrase
            self.privateKey = None
            self.address = ''

        return getAddress()

    def setNetwork(self, network: str):
        pass

    def getAddress(self): 
        if not self.address:
            # address = 
        return 
    
    def getBalance(self, address: str, asset):
        pass

    def transfer(self, txParams):
        pass

    def getFees(self):
        pass

    