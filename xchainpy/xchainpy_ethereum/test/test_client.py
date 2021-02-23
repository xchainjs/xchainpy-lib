import pytest
from xchainpy.xchainpy_ethereum.client import Client


class TestClient:
    mnemonic = open("test_suite/mnemonic", 'r').readline()
    router_abi = open("test_suite/router_abi", 'r').readline()
    token_abi = open("test_suite/token_abi", 'r').readline()
    network = open("test_suite/network", 'r').readline()
    thor_router_address = "0x9d496De78837f5a2bA64Cb40E62c19FBcB67f55a"
    thor_token_address = "0xd601c6A3a36721320573885A8d8420746dA3d7A0"
    client = Client(network, mnemonic)
    client_address = "0x0dC1Ce70a8ddFA3F2070984C35010a285CF0530D"

    def test_is_connected(self):
        assert self.client.is_connected()

    def test_set_network(self):
        self.client.set_network(network=self.network)
        assert self.client.is_connected()

    def test_get_network(self):
        assert self.client.get_network() == self.network

    def test_validate_address(self):
        pass

    def test_get_address(self):
        assert self.client.get_address() == self.client_address

    def test_set_phrase(self):
        assert self.client.set_phrase(self.mnemonic) == self.client_address
        assert self.client.is_connected()

    def test_get_balance(self):
        print(self.client.get_balance())
        print(self.client.get_balance(address="0x3efF38C0e1e5DD6Bd58d3fa79cAecc4Da46C8866"))
        assert(self.client.get_balance(asset='RUNE', contract_abi=self.token_abi,
                                       contract_address=self.thor_token_address)) == 0

    def test_get_contract(self):
        router_contract = self.client.get_contract(self.router_abi, self.thor_router_address)
        assert router_contract.functions.RUNE().call() == self.thor_token_address
        token_contract = self.client.get_contract(self.token_abi, self.thor_token_address)
        assert token_contract.functions.balanceOf(self.client_address).call() == 0

    def test_get_fees(self):
        pass

    def test_write_contract(self):
        old_balance = self.client.get_balance(asset='RUNE', contract_abi=self.token_abi,
                                              contract_address=self.thor_token_address)
        print(old_balance)
        token_contract = self.client.get_contract(self.token_abi, self.thor_token_address)
        print(token_contract.all_functions())
        tx = {
            'nonce': self.client.w3.eth.getTransactionCount(self.client.get_address()),
            'value': self.client.w3.toWei(0, 'ether'),
            'gas': 2000000,
            'gasPrice': self.client.w3.toWei('50', 'gwei'),
        }
        raw_tx = token_contract.functions.giveMeRUNE().buildTransaction(tx)
        print(raw_tx)
        signed_tx = self.client.account.sign_transaction(raw_tx)
        tx_hash = self.client.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        print(tx_hash)
        assert False

    def test_transfer(self):
        # tx_hash = self.client.transfer_ether('0x81941E3DeEeA41b6309045ECbAFd919Db5aF6147', 3)
        # print(tx_hash)
        pass

    def test_get_transaction_data(self):
        tx_hash = '0x7aa171c7c024cbfdcf6e8097fbd8ec18bacf33581acdea0d3923c031a55b931e'
        print(self.client.get_transaction_data(tx_hash))
        pass
