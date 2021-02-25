import pytest
from xchainpy.xchainpy_ethereum.client import Client
import time, json

class TestClient:
    prefix = "resources/ropsten/"
    mnemonic = open(prefix + "mnemonic", 'r').readline()
    router_abi = json.loads(open(prefix + "router_abi", 'r').readline())
    token_abi = json.loads(open(prefix + "token_abi", 'r').readline())
    network = open(prefix + "network", 'r').readline()
    eth_api = open("resources/ether_api", 'r').readline()
    thor_router_address = "0x9d496De78837f5a2bA64Cb40E62c19FBcB67f55a"
    thor_token_address = "0xd601c6A3a36721320573885A8d8420746dA3d7A0"
    client = Client(mnemonic, network, "ropsten", eth_api)
    client_address = "0x0dC1Ce70a8ddFA3F2070984C35010a285CF0530D"
    test_hash = "0x7aa171c7c024cbfdcf6e8097fbd8ec18bacf33581acdea0d3923c031a55b931e"
    test_rune_transfer_hash = "0xa23a19ec29fbc0edc245befe80bda6a29def5b3b4610bf20b670d9e90bfa8095"

    def test_is_connected(self):
        assert self.client.is_connected()

    def test_set_network(self):
        self.client.set_network(network=self.network)
        assert self.client.is_connected()

    def test_get_network(self):
        assert self.client.get_network() == self.network

    def test_validate_address(self):
        assert self.client.validate_address(self.client_address)
        assert self.client.validate_address(self.thor_router_address)
        assert self.client.validate_address(self.thor_token_address)

    def test_get_address(self):
        assert self.client.get_address() == self.client_address

    def test_set_phrase(self):
        assert self.client.set_phrase(self.mnemonic) == self.client_address
        assert self.client.is_connected()

    def test_get_abi(self):
        assert self.client.get_abi(self.thor_router_address) == self.router_abi
        assert self.client.get_abi(self.thor_token_address) == self.token_abi
        self.client.ether_api = None
        assert self.client.get_abi(self.thor_router_address) == self.router_abi
        assert self.client.get_abi(self.thor_token_address) == self.token_abi

    def test_get_contract(self):
        router_contract = self.client.get_contract(self.thor_router_address)
        print(router_contract.all_functions())
        assert router_contract.functions.RUNE().call() == self.thor_token_address
        token_contract = self.client.get_contract(self.thor_token_address)
        print(token_contract.all_functions())
        decimal_place = token_contract.functions.decimals().call()
        assert token_contract.functions.symbol().call() == 'RUNE'
        assert token_contract.functions.maxSupply().call()/10**decimal_place == 500000000.0

    def test_get_balance(self):
        balance = self.client.get_balance()
        balance_address = self.client.get_balance(address=self.client_address)
        assert balance == balance_address
        rune_balance = self.client.get_balance(contract_address=self.thor_token_address)
        rune_balance_address = self.client.get_balance(address=self.client_address,
                                                       contract_address=self.thor_token_address)
        assert rune_balance == rune_balance_address

    def test_get_fees(self):
        self.client.set_gas_strategy("fast")
        fast_fee = self.client.get_fees()
        self.client.set_gas_strategy("medium")
        medium_fee = self.client.get_fees()
        self.client.set_gas_strategy("slow")
        slow_fee = self.client.get_fees()
        assert fast_fee >= medium_fee >= slow_fee

    def test_get_transaction_data(self):
        data = self.client.get_transaction_data(self.test_hash)
        tx_hash = self.client.w3.toHex(data["hash"])
        from_addr = data["from"]
        value = data["value"]
        assert tx_hash == self.test_hash
        assert from_addr == self.client_address
        assert self.client.w3.fromWei(value, 'ether') == 3

    def test_get_transaction_receipt(self):
        data = self.client.get_transaction_receipt(self.test_rune_transfer_hash)
        value = data['logs'][0]['data']
        amount = self.client.w3.toInt(hexstr=value)
        assert amount/10**18 == 1

    def test_transfer_ethereum(self):
        self.client.set_gas_strategy("fast")
        assert self.client.get_balance() > 0.0001
        tx_hash = self.client.transfer('0x81941E3DeEeA41b6309045ECbAFd919Db5aF6147', 0.0001)
        data = self.client.get_transaction_data(tx_hash)
        assert float(self.client.w3.fromWei(data["value"], 'ether')) == 0.0001

    def test_transfer_rune(self):
        self.client.set_gas_strategy("fast")
        dest_addr = '0x81941E3DeEeA41b6309045ECbAFd919Db5aF6147'
        rune_balance = self.client.get_balance(contract_address=self.thor_token_address)
        assert rune_balance > 1
        receipt = self.client.transfer(dest_addr, 1, contract_address=self.thor_token_address)
        value = receipt['logs'][0]['data']
        amount = self.client.w3.toInt(hexstr=value)
        assert amount/10**18 == 1

    # def test_write_contract(self):
    #     old_balance = self.client.get_balance(asset='RUNE', contract_abi=self.token_abi,
    #                                           contract_address=self.thor_token_address)
    #     print(old_balance)
    #     token_contract = self.client.get_contract(self.token_abi, self.thor_token_address)
    #     print(token_contract.all_functions())
    #     tx = {
    #         'nonce': self.client.w3.eth.getTransactionCount(self.client.get_address()),
    #         'value': self.client.w3.toWei(0, 'ether'),
    #         'gas': 2000000,
    #         'gasPrice': self.client.w3.toWei('50', 'gwei'),
    #     }
    #     raw_tx = token_contract.functions.giveMeRUNE().buildTransaction(tx)
    #     print(raw_tx)
    #     signed_tx = self.client.account.sign_transaction(raw_tx)
    #     tx_hash = self.client.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
    #     print(tx_hash)
    #     pass
