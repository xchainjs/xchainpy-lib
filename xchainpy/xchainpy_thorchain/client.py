import asyncio

from typing import Optional
from datetime import datetime
import time

from xchainpy.xchainpy_client import interface
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy.xchainpy_util.asset import Asset
from xchainpy_thorchain import utils

from xchainpy.xchainpy_thorchain.cosmos.sdk_client import CosmosSDKClient
import electrumsv_secp256k1


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
        """Constructor
        
        Client has to be initialised with network type and phrase.
        It will throw an error if an invalid phrase has been passed.
        """
        self.network = network
        self.clientUrl = clientUrl or self.get_default_client_url()
        self.explorerUrl = explorerUrl or self.get_default_explorer_url()
        self.thorClient = self.get_new_thor_client()

        if phrase:
            self.set_phrase(phrase)

    def purge_client(self):
        """Purge client.

        :returns: None
        """
        self.phrase = self.address = ''
        self.private_key = None

    def set_network(self, network):
        """Set/update the current network.

        :param: {Network} network `mainnet` or `testnet`.
        :returns: None
        :raise: {"Network must be provided"}
        Thrown if network has not been set before.
        """
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
        """Get the current network.

        :returns: {Network} The current network. (`mainnet` or `testnet`)
        """
        return self.network

    def setClientUrl(self, clientUrl):
        """Set/update the client URL.

        :param: {string} clientUrl The client url to be set.
        :returns: {void}
        """
        self.clientUrl = clientUrl
        self.thorClient = self.get_new_thor_client()

    def get_default_client_url(self):
        """Get the client url.

        :param: {Network} network
        :returns: {NodeUrl} The client url (both node, rpc) for thorchain based on the network.
        """
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
        """Get the explorer url.

        :returns: {ExplorerUrl} The explorer url (both mainnet and testnet) for thorchain.
        """
        return 'https://testnet.thorchain.net' if self.network == 'testnet' else 'https://thorchain.net'

    def get_prefix(self):
        """Get address prefix based on the network.

        :param: {string} network
        :returns: {string} The address prefix based on the network.
        """
        return 'tthor' if self.network == 'testnet' else 'thor'

    def get_chain_id(self):
        """Get the chain id.

        :returns: {string} The chain id based on the network.
        """
        return 'thorchain'

    def get_new_thor_client(self):
        """Get new thorchain client.

        :returns: {CosmosSDKClient} The new thorchain client.    
        """
        network = self.get_network()
        return CosmosSDKClient(server=self.get_default_client_url()[network]["node"], prefix=self.get_prefix(), derive_path="m/44'/931'/0'/0/0", chain_id=self.get_chain_id())

    def get_private_key(self):
        """Get private key.

        :returns: The private key generated from the given phrase
        :raises: {"Phrase not set"} Throws an error if phrase has not been set before
        """
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
            self.address = self.thorClient.privkey_to_address(
                self.get_private_key())
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
            balances.append(
                {"asset": balance['denom'], "amount": balance['amount']})

        return balances

    async def get_transaction_data(self, tx_id: str):
        """Get the transaction details of a given transaction id

        if you want to give a hash that is for mainnet and the current self.net is 'testnet',
        you should call self.set_network('mainnet') (and vice versa) and then call this method.

        :param tx_id: The transaction id
        :type tx_id: str
        :returns: The transaction details of the given transaction id
        """

        try:
            tx_result = await self.thorClient.txs_hash_get(tx_id)
            if not tx_result:
                raise Exception("transaction not found")
            return tx_result
        except Exception as err:
            raise Exception(err)

    async def transfer(self, amount: int, recipient: str, asset: str = "rune", memo: str = ""):
        """Transfer balances with MsgSend

        :param: amount: 
        :returns: The transaction hash.
        """
        await self.thorClient.make_transaction(self.get_private_key(), self.get_address(), fee_denom=asset, memo=memo)
        self.thorClient.add_transfer(recipient, amount, denom=asset)
        Msg = self.thorClient.get_pushable()
        return await self.thorClient.do_transfer(Msg)

    async def get_fees(self):
        """Get the current fees

        :returns: The fees with three rates
        """

        fee = utils.DEFAULT_GAS_VALUE

        return {
            "fast": fee,
            "fastest": fee,
            "average": fee,
        }
