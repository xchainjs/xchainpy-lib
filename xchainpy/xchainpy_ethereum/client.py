from xchainpy.xchainpy_client.interface import IXChainClient
from xchainpy.xchainpy_crypto import crypto
from web3 import Web3, WebsocketProvider, HTTPProvider, Account
from web3.gas_strategies.time_based import medium_gas_price_strategy, fast_gas_price_strategy, slow_gas_price_strategy
import json, os, asyncio
import faster_than_requests as requests


class IEthereumClient:
    def is_connected(self):
        pass

    def get_abi(self, contract_address):
        pass

    def get_contract(self, contract_address, erc20):
        pass

    def write_contract(self, gas_limit, gas_price, contract_address, func_name, **kwargs):
        pass

    def set_gas_strategy(self, gas_strategy):
        pass

    def transfer(self, dest_addr, quantity, gas_limit, contract_address):
        pass

    def get_transaction_data(self, tx_id):
        pass

    def get_transaction_receipt(self, tx_id):
        pass


class Client(IEthereumClient, IXChainClient):
    script_dir = os.path.dirname(__file__)
    with open(os.path.join(script_dir, "resources/ERC20"), 'r') as f:
        erc20_abi = json.loads(f.read())["abi"]
    network = network_type = ether_api = ''
    gas_strategy = "medium"
    gas_price = None
    w3 = account = None

    def __init__(self,  phrase: str, network: str, network_type: str = "ropsten", ether_api: str = None) -> None:
        """Constructor

        Client has to be initialised with mnemonic phrase, network (infura_api token), network_type ("mainnet" or "ropsten")
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
        """Purge Client

        Returns:
            void

        """
        self.w3 = self.account = None

    def is_connected(self) -> bool:
        """Check Web3 connectivity

        Returns:
            bool

        """
        return self.w3.isConnected()

    def set_network(self, network: str) -> None:
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
        self.w3 = Web3(WebsocketProvider(network))
        if not self.is_connected():
            raise Exception("Infura API error")

    def get_network(self) -> str:
        """Get the current network

        Returns:
            infura websocket api

        """
        return self.network

    def validate_address(self, address: str) -> bool:
        """Check address validity

        Args:
            address: ethereum address

        Returns:
            bool

        """
        return self.w3.isAddress(address)

    def get_address(self) -> str:
        """Get current wallet address

        Returns:
            current wallet address

        """
        return self.account.address

    def set_phrase(self, phrase: str) -> str:
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

    def get_abi(self, contract_address):
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
            if not self.ether_api:
                raise Exception("undefined ether api token")
            if self.network_type == 'mainnet':
                url = f'https://api.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.ether_api}'
            else:
                url = f'https://api-ropsten.etherscan.io/api?module=contract&action=getabi&address={contract_address}&apikey={self.ether_api}'
            r = json.loads(requests.get2json(url))
            if r["status"] != '1':
                raise Exception("error getting abi file")
            with open(path, 'w+') as o:
                o.write(r["result"])
            return json.loads(r["result"])

    def get_contract(self, contract_address, erc20=True):
        """Get Contract object of given address

        Args:
            contract_address: ethereum contract address
            erc20: True if contract = ERC-20, False otherwise

        Returns:
            web3 contract object

        """
        if not erc20:
            return self.w3.eth.contract(abi=self.get_abi(contract_address), address=contract_address)
        return self.w3.eth.contract(abi=self.erc20_abi, address=contract_address)

    def get_balance(self, address=None, contract_address=None) -> float:
        """Get the balance of a erc-20 token

        Args:
            address: By default, it will return the balance of the current wallet. (optional)
            contract_address: If not set, it will return ethereum balance. (optional)

        Returns:
            Balance of the address

        """
        if address:
            if contract_address:
                token_contract = self.get_contract(contract_address)
                decimal = token_contract.functions.decimals().call()
                return token_contract.functions.balanceOf(address).call() / 10**decimal
            return self.w3.fromWei(self.w3.eth.get_balance(address), 'ether')
        elif contract_address:
            token_contract = self.get_contract(contract_address)
            decimal = token_contract.functions.decimals().call()
            return token_contract.functions.balanceOf(self.get_address()).call() / 10**decimal
        return self.w3.fromWei(self.w3.eth.get_balance(self.get_address()), 'ether')

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
            self.w3.eth.setGasPriceStrategy(fast_gas_price_strategy)
        elif gas_strategy == 'medium':
            self.w3.eth.setGasPriceStrategy(medium_gas_price_strategy)
        elif gas_strategy == 'slow':
            self.w3.eth.setGasPriceStrategy(slow_gas_price_strategy)
        else:
            raise Exception("invalid gas strategy")
        self.gas_price = self.w3.eth.generateGasPrice()

    def get_fees(self):
        """Return Gas price using gas_strategy

        Returns:
            gas price in Wei

        """
        return self.gas_price

    def transfer(self, dest_addr, quantity, gas_limit=1000000, gas_price=None, contract_address=None):
        """Transfer ERC20 token with previous configured gas_price

        Args:
            dest_addr: recipient address
            quantity: quantity in ether or in alt coin
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
        nonce = self.w3.eth.getTransactionCount(self.get_address())
        if not contract_address:
            tx = {
                'nonce': nonce,
                'to': dest_addr,
                'value': self.w3.toWei(quantity, 'ether'),
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
            signed_tx = self.account.sign_transaction(tx)
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            return tx_hash
        else:
            tx = {
                'nonce': nonce,
                'gas': gas_limit,
                'gasPrice': gas_price,
            }
            token_contract = self.get_contract(contract_address=contract_address)
            decimal = token_contract.functions.decimals().call()
            raw_tx = token_contract.functions.transfer(dest_addr, quantity*10**decimal).buildTransaction(tx)
            signed_tx = self.account.sign_transaction(raw_tx)
            tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
            return receipt

    def read_contract(self, contract_address, func_to_call, erc20=True, **kwargs):
        contract = self.get_contract(contract_address=contract_address, erc20=erc20)
        return contract.functions[func_to_call](**kwargs).call()

    def write_contract(self, contract_address, func_to_call, erc20=True, gas_limit=1000000, gas_price=None, **kwargs):
        """Write to any contract with any argument, specify whether it's ERC20

        Args:
            contract_address: contract address to interact with
            func_to_call: name of contract function to call
            erc20: True if contract = ERC-20, False otherwise
            gas_limit: 1000000 by default
            gas_price: gas price
            **kwargs: arguments for func_to_call

        Returns:

        """
        nonce = self.w3.eth.getTransactionCount(self.get_address())
        if not gas_price:
            gas_price = self.gas_price
        tx = {
            'nonce': nonce,
            'gas': gas_limit,
            'gasPrice': gas_price,
        }
        smart_contract = self.get_contract(contract_address=contract_address, erc20=erc20)
        contract_func = smart_contract.functions[func_to_call]
        raw_tx = contract_func(**kwargs).buildTransaction(tx)
        signed_tx = self.account.sign_transaction(raw_tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return receipt

    def get_transaction_data(self, tx_id):
        return self.w3.eth.get_transaction(tx_id)

    def get_transaction_receipt(self, tx_id):
        return self.w3.eth.getTransactionReceipt(tx_id)
