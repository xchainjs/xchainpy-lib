import asyncio

from typing import Optional
from datetime import datetime
import time

from xchainpy.xchainpy_client import interface
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy.xchainpy_binance import crypto
from xchainpy.xchainpy_binance import utils
from xchainpy.xchainpy_util.asset import Asset

from xchainpy.xchainpy_thorchain.cosmos.sdk_client import CosmosSDKClient

class IThorchainClient():
    def setClientUrl(self, clientUrl):
        pass

    def setClientUrl(self):
        pass

    def setExplorerUrl(self):
        pass

    def getExplorerNodeUrl(self):
        pass

    def deposit(self):
        pass

class Client(interface.IXChainClient, IThorchainClient):

    derive_path = "m/44'/118'/0'/0/0"
    phrase = address = network = ''
    private_key = None

    def __init__(self, phrase, network="testnet", clientUrl=None, explorerUrl=None):
        self.network = network
        self.clientUrl = clientUrl or self.get_default_client_url()
        self.explorerUrl = explorerUrl or self.get_default_explorer_url()
        self.thorClient = self.get_new_thor_client()

        if phrase:
            self.set_phrase(phrase)

    def purge_client(self):
        self.phrase = self.address = ''
        self.private_key = None

    def set_network(self, network):
        if not network:
            raise Exception('Network must be provided')
        else:
            self.network = network
            self.thorClient = self.get_new_thor_client()
            self.address = ''

    def set_phrase(self, phrase: str):
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")

            self.phrase = phrase
            self.private_key = None
            self.address = ''

        return self.get_address()

    def get_network(self):
        return self.network

    def setClientUrl(self, clientUrl):
        self.clientUrl = clientUrl
        self.thorClient = self.get_new_thor_client()

    def get_default_client_url(self):
        return {
            "testnet": {
                "node": 'https://testnet.thornode.thorchain.info',
                "rpc": 'https://testnet.rpc.thorchain.info',
            },
            "mainnet": {
                "node": 'http://138.68.125.107:1317',
                "rpc": 'http://138.68.125.107:26657',
            },
        }

    def get_default_explorer_url(self):
      return 'https://testnet.thorchain.net' if self.network == 'testnet' else 'https://thorchain.net'

    def get_prefix(self):
        return 'tthor' if self.network == 'testnet' else 'thor'

    def get_chain_id(self):
        return 'thorchain'

    def get_new_thor_client(self):
        network = self.get_network()
        return CosmosSDKClient(server=self.get_default_client_url()[network]["node"] ,prefix=self.get_prefix(), derive_path="m/44'/931'/0'/0/0", chain_id=self.get_chain_id())

    def set_phrase(self, phrase):
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")

            self.phrase = phrase
            self.private_key = None
            self.address = ''

        return self.get_address()

    def get_private_key(self):
        if not self.private_key:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.private_key = self.thorClient.seed_to_privkey(self.phrase)
        
        return self.private_key


    def get_address(self):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if not self.address:
            self.address = self.thorClient.privkey_to_address(self.get_private_key())
            if not self.address:
                raise Exception(
                        "Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key.")
        return self.address

    async def get_balance(self, address=None, asset=None):
        """
         Get the balance of a given address.
        
         :param Address: address By default, it will return the balance of the current wallet. (optional)
         :param Asset: asset If not set, it will return all assets available. (optional)
         :returns: Array<Balance>: The balance of the address.
        """
        if not address:
            address = self.get_address()
        response = await self.thorClient.get_balance(address)
        response = response["result"]

        balances = []
        for balance in response:
            print(balance)
            balances.append({"asset": balance['denom'], "amount": balance['amount']})

        return balances

    async def get_transaction_data(self, tx_id: str):
        try:
            tx_result = await self.thorClient.txs_hash_get(tx_id)
            if not tx_result:
                raise Exception("transaction not found")
            return tx_result
        except Exception as err:
            raise Exception(err)

    async def transfer(self, amount: int, recipient: str, asset: str = "rune", memo: str = ""):
        await self.thorClient.make_transaction(self.get_private_key(), self.get_address(), fee_denom=asset, memo=memo)
        self.thorClient.add_transfer(recipient, amount, denom=asset)
        Msg = self.thorClient.get_pushable()
        return await self.thorClient.do_transfer(Msg)
        

    async def get_fees(self):
        DEFAULT_GAS_VALUE = '10000000'
        fee = DEFAULT_GAS_VALUE
        return {
            "fast": fee,
            "fastest": fee,
            "average": fee,
        }
    


