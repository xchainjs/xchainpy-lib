
from xchainpy.xchainpy_client.interface import IXChainClient


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

    node_url = node_api_key = phrase = net = ''

    def __init__(self, phrase , network='testnet' , node_url = '' , node_api_key = ''):
        
        self.set_network(network)
        self.set_phrase(phrase)

    def set_network(self, network: str):
        if not network :
            raise Exception("Network must be provided")
        else:
            self.net = network