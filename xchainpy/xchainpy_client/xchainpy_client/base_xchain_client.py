import asyncio
from typing import Optional
from datetime import datetime
import time
from abc import ABC, abstractmethod
import json
import http3

from xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy_util.asset import Asset
from xchainpy_util.chain import Chain

from . import interface
from . models import tx_types
from . models.types import XChainClientParams
from . models.types import Network

MAINNET_THORNODE_API_BASE = 'https://thornode.thorchain.info/thorchain'
TESTNET_THORNODE_API_BASE = 'https://testnet.thornode.thorchain.info/thorchain'

class BaseXChainClient(interface.IXChainClient):

    chain = network = phrase = root_derivation_paths = ''

    def __init__(self, chain:Chain, params:XChainClientParams):
        """
        :param chain: chain (xchain_util Chain enum)
        :type chain: Chain
        :param params: params
        :type params: XChainClientParams
        """

        self.chain = chain.value
        self.set_network(params.network or Network.Testnet)
        if params.root_derivation_paths:
            self.root_derivation_paths = params.root_derivation_paths
        # NOTE: we don't call this.setPhrase() to avoid generating an address and paying the perf penalty
        if params.phrase:
            if not xchainpy_crypto.validate_phrase(params.phrase):
                raise Exception('Invalid phrase')
            self.phrase = params.phrase

    def set_network(self, network:Network):
        """Set/update the current network

        :param network: "mainnet" or "testnet"
        :type network: str
        :returns: the client
        :raises: raises if network not provided
        :raises: `Invalid network' if the given network is invalid
        """    
        if not network:
            raise Exception('Network must be provided')

        if type(network) is Network:
            self._network = network.value
        elif type(network) is str and network in ['mainnet', 'MAINNET', 'testnet', 'TESTNET']:
            self._network = network.lower()
        else:
            raise Exception("Invalid network") 

    def get_network(self):
        """Get the current network
        :returns: the current network. (`mainnet` or `testnet`)
        """
        return self.network

    async def get_fee_rate_from_thorchain(self):
        """Get fee rate from thorchain
        :returns: The chain gas_rate
        :raises: 'Thornode API /inbound_addresses does not contain fees for the chain' If gas_rate does not exist for the chain
        """
        data = await self.thornode_api_get('/inbound_addresses')
        if not isinstance(data, list):
            raise Exception('bad response from Thornode API')

        chain_data = filter(lambda x: x.chain == self.chain and type(x.gas_rate) == str, data)

        if not len(chain_data) > 0:
            raise Exception(f'Thornode API /inbound_addresses does not contain fees for {self.chain}')
        
        chain_data = chain_data[0]
        
        return float(chain_data['gas_rate'])

    
    async def thornode_api_get(self, endpoint:str):
        """Thornode api get

        :param endpoint: endpoint
        :type endpoint: str
        :returns: The result of the calling thornode api
        """
        try:
            if self.network == Network.Mainnet.value:
                api_url = f'{MAINNET_THORNODE_API_BASE}'
            else:
                api_url = f'{TESTNET_THORNODE_API_BASE}'

            api_url += endpoint

            client = http3.AsyncClient()
            response = await client.get(api_url)

            if response.status_code == 200:
                return json.loads(response.content.decode('utf-8'))['data']
            else:
                return None
        
        except Exception as err:
            raise Exception(str(err))


    def set_phrase(self, phrase:str, wallet_index:int=0):
        """Set/Update a new phrase

        :param phrase: A new phrase
        :type phrase: str
        :param wallet_index: HD wallet index
        :type wallet_index: int
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """

        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")

            self.phrase = phrase

        return self.get_address(wallet_index)

    def get_full_derivation_path(self, wallet_index:int) -> str:
        """Get full derivation path

        :param wallet_index: HD wallet index
        :type wallet_index: int
        :returns: The derivation path based on the network.
        """
        return f"{self.root_derivation_paths[self.network]}{wallet_index}" if self.root_derivation_paths else ''

    async def purge_client(self):
        """Purge client
        """
        self.phrase = ''


    @abstractmethod
    async def get_fees(self):
        pass
    
    @abstractmethod
    def get_address(self, wallet_index:int) -> str:
        pass

    @abstractmethod
    def get_explorer_url(self) -> str:
        pass

    @abstractmethod
    def get_explorer_address_url(self, address:str) -> str:
        pass

    @abstractmethod
    def get_explorer_tx_url(self, tx_id:str) -> str:
        pass

    @abstractmethod
    def validate_address(self, address:str) -> bool:
        pass
    
    @abstractmethod
    async def get_balance(self, address: str = None, asset: Asset = None):
        pass

    @abstractmethod
    async def get_transactions(self, params:tx_types.TxHistoryParams):
        pass

    @abstractmethod
    async def get_transaction_data(self, tx_id):
        pass

    @abstractmethod
    async def transfer(self, asset: Asset, amount, recipient, memo=''):
        pass

