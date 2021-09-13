import pytest
from xchainpy_ethereum.client import Client
from xchainpy_ethereum.models.asset import Asset
from xchainpy_ethereum.models.client_types import EthereumClientParams
from xchainpy_client.models .types import Network
import json, os, time

ETH_RUNE = Asset("ETH", "RUNE", contract="0x3155BA85D5F96b2d030a4966AF206230e46849cb")
ETH_ETH = Asset("ETH", "ETH")

class TestClient:
    prefix = "../xchainpy_ethereum/resources/mainnet/"
    mnemonic = open(prefix + "mnemonic", 'r').readline()
    sushi_abi = json.loads(open(prefix + "sushi_abi", 'r').readline())
    token_abi = json.loads(open(prefix + "token_abi", 'r').readline())
    wss = open(prefix + "infura", 'r').readline()
    eth_api = open("../xchainpy_ethereum/resources/ether_api", 'r').readline()
    params = EthereumClientParams(wss_provider=wss, etherscan_token=eth_api,
                                  phrase=mnemonic, network=Network.Mainnet)

    sushi_contract_address = "0xcc39592f5cB193a70f262aA301f54DB1d600e6Da"
    test_address = "0xB1aA026725cD51700E674E240D971785F95429FD"
    test_hash = "0x1ea72e2c1721757fd431306cb124e2b75943c5cd20fee5e3e1f79e028c00e99e"
    test_rune_transfer_hash = "0xc8b3e4c68c9d7022290d4203ff867dcef157efb8927ad29e718f97ac5dddaab2"

    @pytest.fixture
    def test_init(self):
        self.client = Client(params=self.params)
        yield
        self.client.purge_client()

    def test_init_param(self):
        with pytest.raises(Exception) as err:
            EthereumClientParams(wss_provider=self.wss, etherscan_token=self.eth_api,
                                 phrase=self.mnemonic, network="invalid")
        assert str(err.value) == "Invalid network"

    def test_init_client(self):
        test_params = EthereumClientParams(wss_provider=self.wss, etherscan_token=self.eth_api,
                                           phrase="invalid", network=Network.Mainnet)
        with pytest.raises(Exception) as err:
            Client(test_params)
        assert str(err.value) == "invalid phrase"

    def test_set_phrase(self, test_init):
        with pytest.raises(Exception) as err:
            self.client.set_phrase(phrase="invalid")
        assert str(err.value) == "invalid phrase"

    def test_web3_provider_connection(self, test_init):
        assert self.client.is_web3_connected()
        test_params = EthereumClientParams(wss_provider="wss://mainnet.network.io/ws/v3/invalid",
                                           etherscan_token=self.eth_api, phrase=self.mnemonic,
                                           network=Network.Mainnet)
        with pytest.raises(Exception) as err:
            Client(test_params)
        with pytest.raises(Exception) as err:
            assert self.client.set_wss_provider(wss_provider="wss://mainnet.network.io/ws/v3/invalid")
        self.client.set_wss_provider(wss_provider=self.wss)
        assert self.client.is_web3_connected()

    def test_get_address(self, test_init):
        assert self.client.get_address() == self.test_address

    def test_validate_address(self, test_init):
        assert self.client.validate_address(self.sushi_contract_address)
        assert self.client.validate_address(ETH_RUNE.contract)

    @pytest.mark.asyncio
    async def test_get_abi(self, test_init):
        if os.path.exists(self.prefix + ETH_RUNE.contract):
            os.remove(self.prefix + ETH_RUNE.contract)
        if os.path.exists(self.prefix + self.sushi_contract_address):
            os.remove(self.prefix + self.sushi_contract_address)
        assert str(await self.client.get_abi(self.sushi_contract_address)) == str(self.sushi_abi)
        assert str(await self.client.get_abi(ETH_RUNE.contract)) == str(self.token_abi)
        self.client.ether_api = None
        assert str(await self.client.get_abi(self.sushi_contract_address)) == str(self.sushi_abi)
        assert str(await self.client.get_abi(ETH_RUNE.contract)) == str(self.token_abi)

    @pytest.mark.asyncio
    async def test_get_contract(self, test_init):
        sushi_contract = await self.client.get_contract(self.sushi_contract_address, erc20=False)
        assert sushi_contract.functions.token0().call() == ETH_RUNE.contract
        token_contract = await self.client.get_contract(ETH_RUNE.contract, erc20=True)
        assert token_contract.functions.symbol().call() == 'RUNE'
        token_contract = await self.client.get_contract(ETH_RUNE.contract, erc20=False)
        decimal_place = token_contract.functions.decimals().call()
        assert token_contract.functions.maxSupply().call()/10**decimal_place == 500000000.0

    @pytest.mark.asyncio
    async def test_get_balance(self, test_init):
        balance = await self.client.get_balance()
        balance_address = await self.client.get_balance(address=self.test_address)
        assert balance == balance_address
        rune_balance = await self.client.get_balance(asset=ETH_RUNE)
        rune_balance_address = await self.client.get_balance(address=self.test_address,
                                                             asset=ETH_RUNE)
        assert rune_balance == rune_balance_address

    # def test_get_fees(self, test_init):
    #     self.client.set_gas_strategy("fast")
    #     fast_fee = self.client.get_fees()
    #     self.client.set_gas_strategy("medium")
    #     medium_fee = self.client.get_fees()
    #     self.client.set_gas_strategy("slow")
    #     slow_fee = self.client.get_fees()
    #     assert fast_fee >= medium_fee >= slow_fee

    def test_get_transaction_data(self, test_init):
        data = self.client.get_transaction_data(self.test_hash)
        tx_hash = self.client.w3.toHex(data["hash"])
        from_addr = data["from"]
        value = data["value"]
        assert tx_hash == self.test_hash
        assert float(self.client.w3.fromWei(value, 'ether')) == 0.7

    def test_get_transaction_receipt(self, test_init):
        data = self.client.get_transaction_receipt(self.test_rune_transfer_hash)
        value = data['logs'][0]['data']
        amount = self.client.w3.toInt(hexstr=value)
        assert amount/10**18 == 1

    # def test_transfer_rune(self, test_init):
    #     self.client.set_gas_strategy("fast")
    #     dest_addr = self.client.w3.toChecksumAddress('0x5039c76445efcfa78d91b8974c100151634cbf2d')
    #     rune_balance = self.client.get_balance(contract_address=self.thor_token_address)
    #     assert rune_balance > 1
    #     receipt = self.client.transfer(dest_addr, 1, contract_address=self.thor_token_address)
    #     value = receipt['logs'][0]['data']
    #     amount = self.client.w3.toInt(hexstr=value)
    #     assert amount/10**18 == 1
    #
    # def test_transfer_ethereum(self, test_init):
    #     self.client.set_gas_strategy("fast")
    #     assert self.client.get_balance() > 0.0001
    #     tx_hash = self.client.transfer('0x81941E3DeEeA41b6309045ECbAFd919Db5aF6147', 0.0001)
    #     data = self.client.get_transaction_data(tx_hash)
    #     assert float(self.client.w3.fromWei(data["value"], 'ether')) == 0.0001

    @pytest.mark.asyncio
    async def test_read_contract(self, test_init):
        # assert await self.client.read_contract(self.thor_token_address, "balanceOf", self.client.get_address()) / 10**18\
        #        == await self.client.get_balance(contract_address=self.thor_token_address)
        assert await self.client.read_contract(self.sushi_contract_address, "factory", erc20=False) == "0xC0AEe478e3658e2610c5F7A4A2E1777cE9e4f2Ac"

    # def test_write_contract_token(self, test_init):
    #     old_balance = self.client.get_balance(contract_address=self.thor_token_address)
    #     func_to_call = "giveMeRUNE"
    #     self.client.set_gas_strategy("fast")
    #     tx_receipt = self.client.write_contract(self.thor_token_address, func_to_call, erc20=False)
    #     new_balance = self.client.get_balance(contract_address=self.thor_token_address)
    #     assert new_balance > old_balance

    # def test_write_contract_router(self):
    #     old_balance = self.client.get_balance(contract_address=self.thor_token_address)
    #     func_to_call = "deposit"
    #     asgard_address = self.client.w3.toChecksumAddress("0x5319f65449bf48cf979ba8e839e80415d2395284")
    #     amount = 1000*10**18
    #     memo = "switch:tthor1vecuqg5tejlxncykw6dfkj6hgkv49d59lc0z6j"
    #     x = self.client.get_contract(contract_address=self.thor_router_address, erc20=False)
    #     self.client.set_gas_strategy("fast")
    #     # <Function deposit(address,address,uint256,string)>
    #     tx_receipt = self.client.write_contract(self.thor_router_address, func_to_call,
    #                                             asgard_address, self.thor_token_address, amount,
    #                                             memo, erc20=False)
    #     new_balance = self.client.get_balance(contract_address=self.thor_token_address)
    #     assert new_balance < old_balance

    # def test_fast_write(self):
    #     func_to_call = "xxx"
    #     self.client.set_gas_strategy("fast")
    #     nonce = self.client.w3.eth.getTransactionCount(self.client.get_address())
    #     for i in range(10):
    #         tx_receipt = self.client.write_contract(self.thor_token_address, func_to_call, erc20=False, nonce=nonce+i)