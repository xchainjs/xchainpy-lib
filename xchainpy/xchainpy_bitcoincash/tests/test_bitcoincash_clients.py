import pytest
from xchainpy_client.models import tx_types
from xchainpy_client.models.types import Network
from xchainpy.xchainpy_bitcoincash.xchainpy_bitcoincash.models.client_types import BitcoincashClientParams, BitcoincashTxParams
from xchainpy.xchainpy_bitcoincash.xchainpy_bitcoincash.client import Client
from xchainpy_util.asset import AssetBCH


class TestBitcoincashClient:
    memo = 'SWAP:THOR.RUNE'
    phrase = 'atom green various power must another rent imitate gadget creek fat then'
    testnet_address_path0 = 'bchtest:qpd7jmj0hltgxux06v9d9u6933vq7zd0kyjlapya0g'
    testnet_address_path1 = 'bchtest:qrkd7dhu7zcmn6wwvj3p4aueslycqchj5vxx3stmjz'
    mainnet_address_path0 = 'bitcoincash:qp4kjpk684c3d9qjk5a37vl2xn86wxl0f5j2ru0daj'
    mainnet_address_path1 = 'bitcoincash:qr4jrkhu3usuk8ghv60m7pg9eywuc79yqvd0wxt2lm'
    
    @pytest.fixture
    def client(self):
        self.client = Client(BitcoincashClientParams(network='testnet', phrase=self.phrase))
        yield
        self.client.purge_client()

    def test_set_phrase_should_return_correct_address(self, client):
        self.client.set_network('testnet')
        assert self.client.set_phrase(self.phrase) == self.testnet_address_path0

        self.client.set_network('mainnet')
        assert self.client.set_phrase(self.phrase) == self.mainnet_address_path0

    def test_set_phrase_with_derivation_path_should_return_correct_address(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase)
        self.client.get_address(index=1) == self.testnet_address_path1

        self.client.set_network('mainnet')
        self.client.set_phrase(self.phrase)
        self.client.get_address(index=1) == self.mainnet_address_path1

    def test_invalid_phrase(self):
        with pytest.raises(Exception) as err:
            assert Client(BitcoincashClientParams(phrase='invalid phrase'))
        assert str(err.value) == "invalid phrase"

    def test_right_phrase(self, client):
        assert self.client.set_phrase(self.phrase) == self.testnet_address_path0

    def test_validate_address(self, client):
        assert self.client.validate_address(address=self.mainnet_address_path0)
        assert self.client.validate_address(address=self.testnet_address_path0)

    def test_should_return_valid_explorer_url(self, client):
        assert self.client.get_explorer_url() == 'https://www.blockchain.com/bch-testnet'
        self.client.set_network(Network.Mainnet)
        assert self.client.get_explorer_url() == 'https://www.blockchain.com/bch'

    def test_should_retrun_valid_explorer_address_url(self, client):
        assert self.client.get_explorer_address_url('testAddressHere') == 'https://www.blockchain.com/bch-testnet/address/testAddressHere'
        self.client.set_network(Network.Mainnet)
        assert self.client.get_explorer_address_url('anotherTestAddressHere') == 'https://www.blockchain.com/bch/address/anotherTestAddressHere'

    def test_should_retrun_valid_explorer_tx_url(self, client):
        assert self.client.get_explorer_tx_url('testTxHere') == 'https://www.blockchain.com/bch-testnet/tx/testTxHere'
        self.client.set_network(Network.Mainnet)
        assert self.client.get_explorer_tx_url('anotherTestTxHere') == 'https://www.blockchain.com/bch/tx/anotherTestTxHere'

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        balance = await self.client.get_balance('bchtest:qz35h5mfa8w2pqma2jq06lp7dnv5fxkp2svtllzmlf')
        balance = balance[0]
        assert balance.asset == AssetBCH
        assert isinstance(balance.amount, float)

    @pytest.mark.asyncio
    async def test_get_transaction_with_hash(self, client):
        tx_data = await self.client.get_transaction_data('0d5764c89d3fbf8bea9b329ad5e0ddb6047e72313c0f7b54dcb14f4d242da64b')
        assert tx_data.tx_hash == '0d5764c89d3fbf8bea9b329ad5e0ddb6047e72313c0f7b54dcb14f4d242da64b'
        assert len(tx_data.tx_from) == 1
        assert tx_data.tx_from[0].address == 'bchtest:qzyrvsm6z4ucrhaq4zza3wylre7mavvldgr67jrxt4'
        assert str(tx_data.tx_from[0].amount) == '0.04008203'

        assert len(tx_data.tx_to) == 2
        assert tx_data.tx_to[0].address == 'bchtest:qq235k7k9y5cwf3s2vfpxwgu8c5497sxnsdnxv6upc'
        assert str(tx_data.tx_to[0].amount) == '0.04005704'

    @pytest.mark.asyncio
    async def test_get_transactions(self, client):
        tx_page = await self.client.get_transactions(tx_types.TxHistoryParams(address='bchtest:qz35h5mfa8w2pqma2jq06lp7dnv5fxkp2svtllzmlf', limit=1))
        tx_data = tx_page.txs[0]
        assert tx_data.tx_hash == '0957b51a39d6e67a7a3ced07b49a1102006cb51cea7c82b5a949a8678f3ac35c'
        assert len(tx_data.tx_from) == 1
        assert tx_data.tx_from[0].address == 'bchtest:qzmpc0fz8tdz9kkfhxzmu0rt6d23dvyusugshegndx'
        assert tx_data.tx_from[0].amount == 0.00003834

        assert len(tx_data.tx_to) == 2
        assert tx_data.tx_to[0].address == 'bchtest:qz35h5mfa8w2pqma2jq06lp7dnv5fxkp2svtllzmlf'
        assert tx_data.tx_to[0].amount == 0.000006


    @pytest.mark.asyncio
    async def test_transfer_with_memo_and_fee_rate(self, client):
        fee_rates = await self.client.get_fee_rates()
        fee_rate = fee_rates.fast
        balance = await self.client.get_balance('bchtest:qzt6sz836wdwscld0pgq2prcpck2pssmwge9q87pe9')
        balance = balance[0]
        if balance.amount > 0:
            amount = 0.00000001
            tx_id = await self.client.transfer(BitcoincashTxParams(amount, 'bchtest:qzt6sz836wdwscld0pgq2prcpck2pssmwge9q87pe9', self.memo, fee_rate))
            assert tx_id
            
    @pytest.mark.asyncio
    async def test_fee_and_rates_normal_tx(self, client):
        fees_and_rates = await self.client.get_fees_with_rates()
        fees = fees_and_rates.fees
        rates = fees_and_rates.rates
        assert fees.fastest
        assert fees.fast
        assert fees.average
        assert rates.fastest
        assert rates.fast
        assert rates.average

    @pytest.mark.asyncio
    async def test_fee_and_rates_with_memo(self, client):
        fees_and_rates = await self.client.get_fees_with_rates(self.memo)
        fees = fees_and_rates.fees
        rates = fees_and_rates.rates
        assert fees.fastest
        assert fees.fast
        assert fees.average
        assert rates.fastest
        assert rates.fast
        assert rates.average

    @pytest.mark.asyncio
    async def test_estimated_fees_normal_tx(self, client):
        fees = await self.client.get_fees()
        assert fees.fastest
        assert fees.fast
        assert fees.average

    @pytest.mark.asyncio
    async def test_different_fees_normal_tx(self, client):
        fees = await self.client.get_fees()

        assert fees.fastest > fees.fast
        assert fees.fast > fees.average