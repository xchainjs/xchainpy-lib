import pytest
from xchainpy.xchainpy_bitcoincash.client import Client
from xchainpy.xchainpy_util.asset import Asset


class TestBitcoincashClient:
    memo = 'SWAP:THOR.RUNE'
    phrase = 'atom green various power must another rent imitate gadget creek fat then'
    testnet_address = 'bchtest:qpd7jmj0hltgxux06v9d9u6933vq7zd0kyjlapya0g'
    mainnet_address = 'bitcoincash:qp4kjpk684c3d9qjk5a37vl2xn86wxl0f5j2ru0daj'

    bch_asset = Asset('BCH', 'BCH')
    
    @pytest.fixture
    def client(self):
        self.client = Client(phrase=self.phrase, network='testnet')
        yield
        self.client.purge_client()

    def test_set_phrase_should_return_correct_address(self, client):
        self.client.set_network('testnet')
        assert self.client.set_phrase(self.phrase) == self.testnet_address

        self.client.set_network('mainnet')
        assert self.client.set_phrase(self.phrase) == self.mainnet_address


    def test_invalid_phrase(self):
        with pytest.raises(Exception) as err:
            assert Client(phrase='Invalid Phrase')
        assert str(err.value) == "Invalid Phrase"

    def test_right_phrase(self, client):
        assert self.client.set_phrase(self.phrase) == self.testnet_address

    def test_validate_address(self, client):
        assert self.client.validate_address(address=self.mainnet_address)
        assert self.client.validate_address(address=self.testnet_address)

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        balance = await self.client.get_balance()
        assert balance.asset == self.bch_asset
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
    async def test_transfer_with_memo_and_fee_rate(self, client):
        fee_rates = await self.client.get_fee_rates()
        fee_rate = fee_rates['fast']
        balance = await self.client.get_balance()
        if balance.amount > 0:
            amount = 0.00000001
            tx_id = await self.client.transfer(amount, 'bchtest:qzt6sz836wdwscld0pgq2prcpck2pssmwge9q87pe9', self.memo, fee_rate)
            assert tx_id
            
    @pytest.mark.asyncio
    async def test_fee_and_rates_normal_tx(self, client):
        fees_and_rates = await self.client.get_fees_with_rates()
        fees = fees_and_rates['fees']
        rates = fees_and_rates['rates']
        assert fees['fastest']
        assert fees['fast']
        assert fees['average']
        assert rates['fastest']
        assert rates['fast']
        assert rates['average']

    @pytest.mark.asyncio
    async def test_fee_and_rates_with_memo(self, client):
        fees_and_rates = await self.client.get_fees_with_rates(self.memo)
        fees = fees_and_rates['fees']
        rates = fees_and_rates['rates']
        assert fees['fastest']
        assert fees['fast']
        assert fees['average']
        assert rates['fastest']
        assert rates['fast']
        assert rates['average']

    @pytest.mark.asyncio
    async def test_estimated_fees_normal_tx(self, client):
        fees = await self.client.get_fees()
        assert fees['fastest']
        assert fees['fast']
        assert fees['average']

    @pytest.mark.asyncio
    async def test_different_fees_normal_tx(self, client):
        fees = await self.client.get_fees()

        assert fees['fastest'] > fees['fast']
        assert fees['fast'] > fees['average']