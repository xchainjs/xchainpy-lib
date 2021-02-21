from xchainpy.xchainpy_bitcoincash.crypto import mnemonic_to_private_key, private_key_to_address, private_key_to_public_key
from mnemonic.mnemonic import Mnemonic
from xchainpy.xchainpy_crypto.crypto import validate_phrase
from xchainpy.xchainpy_bitcoincash.utils import ClientUrl, get_derive_path
from xchainpy.xchainpy_client.interface import IXChainClient


class IBitcoinCashClient():
    def derive_path(self) -> str :
        pass
    def get_fees_with_rates(self , memo = None):
        pass
    def get_fees_with_memo(self):
        pass
    def get_fee_rates():
        pass

class Client(IBitcoinCashClient , IXChainClient):
    def __init__(self, client_url : ClientUrl , phrase : str , network = 'testnet'):
        self.network = network
        self.client_url = client_url if client_url else self.get_default_client_url()
        self.set_phrase(phrase)

    def get_default_client_url(self) -> ClientUrl:
        return ClientUrl("https://api.haskoin.com/bchtest" ,"https://api.haskoin.com/bch")

    def set_phrase(self, phrase: str):
        if validate_phrase(phrase):
            self.phrase = phrase
            self.address = self.get_address()
            return self.address
        else:
            raise Exception("Invalid Phrase")

    def get_address(self):
        if self.phrase:
            try:
                priv_key = self.get_private_key(self.phrase)
                address = private_key_to_address(priv_key)
                return str(address)
            except:
                print('Address not defined')
        else:
            raise Exception("Phrase must be provided")

    def get_private_key(self , phrase : str):
        try:
            privKey = mnemonic_to_private_key(phrase,self.network)
            return privKey
        except:
            raise Exception("Invalid Phrase")


    def derive_path(self):
        return get_derive_path().testnet if self.network == 'testnet' else get_derive_path().mainnet