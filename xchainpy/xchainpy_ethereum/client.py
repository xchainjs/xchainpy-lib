from xchainpy.xchainpy_client.interface import IXChainClient
from xchainpy.xchainpy_crypto import crypto
from web3 import Web3, WebsocketProvider, HTTPProvider, Account
import json, os, asyncio
import faster_than_requests as requests


class IEthereumClient:
    def is_connected(self):
        pass

    def get_abi(self, contract_address):
        pass

    def get_contract(self, contract_address):
        pass

    def write_contract(self, contract_address, function_index):
        pass


class Client(IEthereumClient, IXChainClient):
    network = network_type = ether_api = ''
    w3 = account = None

    def __init__(self,  phrase: str, network: str, network_type: str = "ropsten", ether_api: str = None) -> None:
        """ Constructor

        Client has to be initialised with mnemonic phrase, network (infura_api), network_type ("mainnet" or "ropsten")
        It will throw an error if an invalid phrase or network has been passed.

        Args:
            phrase: phrase of wallet (mnemonic) will be set to the Class
            network: infura websocket api endpoint of the selected network_type
            network_type: network type can either be `mainnet` or 'ropsten'

        Returns:
            void

        """
        if network_type != "ropsten" and network_type != "mainnet":
            raise Exception('Network type has to be ropsten or mainnet')
        self.ether_api = ether_api
        self.network_type = network_type
        self.set_network(network)
        self.set_phrase(phrase)
        print(f'connected to wallet address{self.account.address}')

    def purge_client(self) -> None:
        """ Purge Client

        Returns:
            void

        """
        self.w3 = self.account = None

    def is_connected(self) -> bool:
        """ Check Web3 connectivity

        Returns:
            bool

        """
        return self.w3.isConnected()

    def set_network(self, network: str) -> None:
        """ Set/update the current network

        It will throw an error if an invalid phrase or network has been passed.

        Args:
            network: infura websocket api endpoint of the selected network_type

        Returns:
            void

        Raises:
            Exception: "Network must be provided". -> Thrown if network has not been set before.

        """
        self.network = network
        self.w3 = Web3(WebsocketProvider(network))
        if not self.is_connected():
            raise Exception("Infura API error")

    def get_network(self) -> str:
        """ Get the current network

        Returns:
            infura websocket api

        """
        return self.network

    def validate_address(self, address: str) -> bool:
        """ Check address validity

        Args:
            address: ethereum address

        Returns:
            bool

        """
        return self.w3.isAddress(address)

    def get_address(self) -> str:
        """ Get current wallet address

        Returns:
            current wallet address

        """
        return self.account.address

    def set_phrase(self, phrase: str) -> str:
        """ Set/Update a new phrase

        Args:
            phrase: A new phrase

        Returns:
            The address of the given phrase

        Raises:
            'Invalid Phrase' if the given phrase is invalid

        """
        if not crypto.validate_phrase(phrase):
            raise Exception("invalid phrase")
        Account.enable_unaudited_hdwallet_features()
        self.account = self.w3.eth.account.from_mnemonic(mnemonic=phrase)
        return self.get_address()

    async def get_abi(self, contract_address):
        """ Get abi description of a given contract

        Args:
            contract_address: contract address

        Returns:
            abi description

        """
        path = f'resources/{self.network_type}/{contract_address}'
        if os.path.exists(path):
            return json.loads(open(path, 'r').readline())
        else:
            if not self.ether_api:
                raise Exception("undefined ether api token")
            if self.network_type == 'mainnet':
                url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.ether_api}'
            else:
                url = f'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.ether_api}'
            r = json.loads(requests.get2json(url))
            if r["status"] != '1':
                raise Exception("error getting abi file")
            open(path, 'w+').write(r["result"])
            return r["result"]

    def get_contract(self, contract_address):
        """ Get Contract object of given address

        Args:
            contract_address: ethereum contract address

        Returns:
            web3 contract object

        """
        return self.w3.eth.contract(abi=self.get_abi(contract_address), address=contract_address)

    async def get_balance(self, address=None, contract_address=None) -> str:
        """ Get the balance of a given address

        Args:
            address: By default, it will return the balance of the current wallet. (optional)
            contract_address: If not set, it will return ethereum balance. (optional)

        Returns:
            Balance of the address

        """
        if address:
            if contract_address:
                token_contract = self.get_contract(contract_address)
                return token_contract.functions.balanceOf(address).call()
            return self.w3.fromWei(self.w3.eth.get_balance(address), 'ether')
        elif contract_address:
            token_contract = self.get_contract(contract_address)
            return token_contract.functions.balanceOf(self.get_address()).call()
        return self.w3.fromWei(self.w3.eth.get_balance(self.get_address()), 'ether')

    def get_fees(self):
        pass

    def transfer_ether(self, dest_addr, quantity):
        nonce = self.w3.eth.getTransactionCount(self.get_address())
        tx = {
            'nonce': nonce,
            'to': dest_addr,
            'value': self.w3.toWei(quantity, 'ether'),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
        }
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash

    def transfer_alt(self, dest_addr, quantity, contract):
        nonce = self.w3.eth.getTransactionCount(self.get_address())
        pass

    def write_contract(self, contract_address, function_index):
        pass

    def get_transaction_data(self, txId: str):
        return self.w3.eth.get_transaction(txId)