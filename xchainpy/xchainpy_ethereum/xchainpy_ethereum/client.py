import asyncio
import json
import os
import requests
from web3 import Web3, WebsocketProvider, Account
from web3.gas_strategies.time_based import slow_gas_price_strategy, medium_gas_price_strategy, fast_gas_price_strategy
from xchainpy_ethereum.models.asset import Asset
from xchainpy_client import interface
from xchainpy_crypto import crypto


class IEthereumClient:
    def is_connected(self):
        pass

    async def get_abi(self, contract_address):
        pass

    async def get_contract(self, contract_address, erc20=True):
        pass

    async def read_contract(self, contract_address, func_to_call, *args, erc20=True):
        pass

    async def write_contract(self, contract_address, func_to_call, *args, erc20=True, gas_limit=1000000, gas_price=None, nonce=None):
        pass

    def set_gas_strategy(self, gas_strategy):
        pass

    async def transfer(self, asset: Asset, amount, recipient, gas_limit=1000000, gas_price=None):
        pass

    def get_transaction_data(self, tx_id):
        pass

    def get_transaction_receipt(self, tx_id):
        pass

    async def get_balance(self, asset: Asset=None, address=None):
        pass


class Client(interface.IXChainClient, IEthereumClient):
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, "resources/ERC20"), 'r') as f:
        erc20_abi = json.loads(f.read())["abi"]
    network = network_type = ether_api = ''
    gas_strategy = "medium"
    gas_price = None
    w3 = account = None

    def __init__(self,  phrase: str, network: str, network_type: str = "ropsten", ether_api: str = None):
        """Constructor

        Client has to be initialised with mnemonic phrase, network (infura_api token), network_type ("mainnet" or "ropsten"),
        ether_api: etherscan api token.
        It will throw an error if an invalid phrase or network has been passed.

        Args:
            phrase: phrase of wallet (mnemonic) will be set to the Class
            network: infura websocket api endpoint of the selected network_type
            network_type: network type can either be `mainnet` or 'ropsten'
            ether_api: etherscan API token, used for downloading non ERC20 contract ABI

        Returns:
            void

        """
        if network_type != "ropsten" and network_type != "mainnet":
            raise Exception('Network type has to be ropsten or mainnet')
        self.ether_api = ether_api
        self.network_type = network_type
        os.makedirs(os.path.join(self.script_dir, f'resources/{network_type}'), exist_ok=True)
        self.set_network(network)
        self.set_phrase(phrase)

    def purge_client(self):
        """Purge Client

        Delete Account

        Returns:
            void

        """
        self.w3 = self.account = None

    def is_connected(self):
        """Check Web3 connectivity

        Returns:
            bool

        """
        return self.w3.isConnected()

    def set_network(self, network: str):
        """Set/update the current network

        It will throw an error if an invalid phrase or network has been passed.

        Args:
            network: infura websocket api endpoint of the selected network_type

        Returns:
            void

        Raises:
            Exception: "Network must be provided". -> Thrown if network has not been set before.

        """
        self.network = network
        if self.network_type not in network:
            raise Exception("invalid network type")
        self.w3 = Web3(WebsocketProvider(network))
        if not self.is_connected():
            raise Exception("Infura API error")

    def get_network(self):
        """Get the current network

        Returns:
            infura websocket api

        """
        return self.network

    def validate_address(self, address: str):
        """Check address validity

        Args:
            address: ethereum address

        Returns:
            bool

        """
        return self.w3.isAddress(address)

    def get_address(self):
        """Get current wallet address

        Returns:
            current wallet address

        """
        return self.account.address

    def set_phrase(self, phrase: str):
        """Set/Update a new phrase

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
        """Get abi description of a non ERC-20 contract

        Args:
            contract_address: contract address

        Returns:
            abi description[json]

        """
        path = os.path.join(self.script_dir, f'resources/{self.network_type}/{contract_address}')
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.loads(f.read())
        else:
            resource_path = os.path.join(self.script_dir, f'resources/{self.network_type}')
            os.makedirs(resource_path, exist_ok=True)
            if not self.ether_api:
                raise Exception("undefined ether api token")
            if self.network_type == 'mainnet':
                url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.ether_api}'
            else:
                url = f'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.ether_api}'
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
            r = requests.get(url, headers=headers).json()
            if r["status"] != '1':
                raise Exception("error getting abi file")
            with open(path, 'w+') as o:
                o.write(r["result"])
            return json.loads(r["result"])

    async def get_contract(self, contract, erc20=True):
        """Get Contract object of given address
        if you are calling non-generic functions you have to pass in erc20=false

        Args:
            address: ethereum contract address
            erc20: True if contract = ERC-20, False otherwise

        Returns:
            web3 contract object

        """
        abi = self.erc20_abi
        if not erc20:
            abi = await self.get_abi(contract)
        return self.w3.eth.contract(abi=abi, address=contract)

    async def get_balance(self, asset=None, address=None):
        """Get the balance of a erc-20 token

        Args:
            asset: asset object, if None, return balance of ethereum. (optional)
            address: By default, it will return the balance of the current wallet. (optional)

        Returns:
            Balance of the address

        """
        if not address:
            address = self.get_address()
        if not asset:
            return self.w3.fromWei(self.w3.eth.get_balance(address), 'ether')
        else:
            assert asset.contract, "asset contract address not set"
            contract = await self.get_contract(asset.contract)
            decimal = contract.functions.decimals().call()
            return contract.functions.balanceOf(address).call() / 10 ** decimal

    def set_gas_strategy(self, gas_strategy) -> None:
        """Set Gas fee calculation parameter

        fast: transaction mined within 60 seconds
        medium: transaction mined within 5 minutes
        slow: transaction mined within 1 hour

        Args:
            gas_strategy: ['fast', 'medium', 'slow']

        Returns:
            void
        """
        if gas_strategy == "fast":
            self.w3.eth.set_gas_price_strategy(fast_gas_price_strategy)
        elif gas_strategy == 'medium':
            self.w3.eth.set_gas_price_strategy(medium_gas_price_strategy)
        elif gas_strategy == 'slow':
            self.w3.eth.set_gas_price_strategy(slow_gas_price_strategy)
        else:
            raise Exception("invalid gas strategy")
        self.gas_price = self.w3.eth.generate_gas_price()

    def get_fees(self):
        """Return Gas price using gas_strategy

        Returns:
            gas price in Wei

        """
        return self.gas_price

    async def transfer(self, asset: Asset, amount, recipient, gas_limit=1000000, gas_price=None):
        """Transfer ERC20 token with previous configured gas_price

        Args:
            recipient: recipient address
            amount: amount in ether or in alt coin
            gas_limit: gas limit using gas price
            gas_price: gas price in wei
            contract_address: for assets other than ether

        Returns:
            tx_hash(str)

        """
        if not gas_price:
            gas_price = self.get_fees()
            if not gas_price:
                raise Exception("gas_price not set")
        nonce = self.w3.eth.get_transaction_count(self.get_address())
        if asset.symbol == 'ETH':
            tx = {
                'nonce': nonce,
                'to': recipient,
                'value': self.w3.toWei(amount, 'ether'),
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            return tx_hash
        else:
            tx = {
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
            token_contract = await self.get_contract(contract_address=asset.ticker)
            decimal = token_contract.functions.decimals().call()
            raw_tx = token_contract.functions.transfer(recipient, amount*10**decimal).buildTransaction(tx)
            signed_tx = self.account.sign_transaction(raw_tx)
            tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            return receipt

    async def read_contract(self, contract_address, func_to_call, *args, erc20=True):
        contract = await self.get_contract(contract_address=contract_address, erc20=erc20)
        return contract.functions[func_to_call](*args).call()

    async def write_contract(self, contract_address, func_to_call, *args, erc20=True, gas_limit=1000000, gas_price=None, nonce=None, eth_to_be_sent=0):
        """Write to any contract with any argument, specify whether it's ERC20

        Args:
            contract_address: contract address to interact with
            func_to_call: name of contract function to call
            erc20: True if contract = ERC-20, False otherwise
            gas_limit: 1000000 by default
            gas_price: gas price
            **kwargs: arguments for func_to_call
            nonce: provide nonce for faster execution
            eth_to_be_sent: in case ethereum needed to be sent

        Returns:

        """
        if not nonce:
            nonce = self.w3.eth.get_transaction_count(self.get_address())
        if not gas_price:
            gas_price = self.gas_price
        if not gas_price:
            raise Exception("provide gas price or call set_gas_strategy()")
        if eth_to_be_sent != 0:
            tx = {
                'nonce': nonce,
                'value': self.w3.toWei(eth_to_be_sent, 'ether'),
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
        else:
            tx = {
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
        smart_contract = await self.get_contract(contract_address=contract_address, erc20=erc20)
        contract_func = smart_contract.functions[func_to_call]
        raw_tx = contract_func(*args).buildTransaction(tx)
        signed_tx = self.account.sign_transaction(raw_tx)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(transaction_hash=tx_hash, timeout=600)
        return receipt

    def get_transaction_data(self, tx_id):
        """
        Args:
            tx_id:
        Returns:
        AttributeDict({
            'blockHash': '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd',
            'blockNumber': 46147,
            'from': '0xA1E4380A3B1f749673E270229993eE55F35663b4',
            'gas': 21000,
            'gasPrice': 50000000000000,
            'hash': '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060',
            'input': '0x',
            'nonce': 0,
            'to': '0x5DF9B87991262F6BA471F09758CDE1c0FC1De734',
            'transactionIndex': 0,
            'value': 31337,
        })
        """
        return self.w3.eth.get_transaction(tx_id)

    def get_transaction_receipt(self, tx_id):
        return self.w3.eth.get_transaction_receipt(tx_id)
