
from xchainpy.xchainpy_crypto.crypto import validate_phrase
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
        self.set_node_url(node_url)
        self.set_node_api_key(node_api_key)
        self.set_phrase(phrase)

    def set_network(self, network: str):
        if not network :
            raise Exception("Network must be provided")
        else:
            if not network in ['testnet' , 'mainnet']:
                raise Exception('Invalid network')
            else:
                self.net = network
    
    def set_node_url(self , url : str):
        if not url:
            raise Exception("Node url must be provided")
        else:
            self.node_url = url

    def set_node_api_key(self , node_api_key):
        if not node_api_key:
            raise Exception("Node API key must be provided")
        else:
            self.set_node_api_key = node_api_key
    
    def set_phrase(self , phrase : str):
        if validate_phrase(phrase):
            self.phrase = phrase
            address = self.get_address()
            return address
        else:
            raise Exception("Invalid Phrase")