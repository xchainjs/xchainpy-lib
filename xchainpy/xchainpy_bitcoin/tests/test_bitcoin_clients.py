import pytest
from xchainpy_bitcoin.client import Client
from xchainpy_util.asset import Asset
from xchainpy_client.models import tx_types
from xchainpy_bitcoin.const import *


class TestBitcoinClient:

    # please don't touch the tBTC in these
    phrase = 'atom green various power must another rent imitate gadget creek fat then'
    testnetaddress = 'tb1q2pkall6rf6v6j0cvpady05xhy37erndvku08wp'
    btc_asset = Asset('BTC', 'BTC')
    memo = 'SWAP:THOR.RUNE'

    phrase_for_tx1 = 'caution pear excite vicious exotic slow elite marble attend science strategy rude'
    testnetaddress_for_tx1 = 'tb1qxe0e8793v3z0v0h2l3nglzg85k2jdx04vx088z'

    phrase_for_tx2 = 'theme neither sun invite illness chat project enough answer spray visual zoo'
    testnetaddress_for_tx2 = 'tb1qymzatfxg22vg8adxlnxt3hkfmzl2rpuzpk8kcf'

    address_for_transactions = 'tb1q04y2lnt0ausy07vq9dg5w2rnn9yjl3rzgjhra4'

    @pytest.fixture
    def client(self):
        self.client = Client(self.phrase, network='testnet')
        yield
        self.client.purge_client()

    def test_right_address(self, client):
        assert self.client.get_address() == self.testnetaddress

    def test_invalid_phrase(self):
        with pytest.raises(Exception) as err:
            assert Client(phrase='Invalid Phrase')
        assert str(err.value) == "Invalid Phrase"

    def test_right_phrase(self, client):
        assert self.client.set_phrase(self.phrase) == self.testnetaddress

    def test_validate_address(self, client):
        assert self.client.validate_address(
            network=self.client.net, address=self.testnetaddress)

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        assert await self.client.get_balance()

    @pytest.mark.asyncio
    async def test_has_no_balances(self, client):
        self.client.set_network('mainnet')
        balance = await self.client.get_balance()
        assert balance.amount == 0

    @pytest.mark.asyncio
    async def test_equal_balances_when_call_getbalance_twice(self, client):
        balance1 = await self.client.get_balance()
        balance2 = await self.client.get_balance()
        assert balance1.amount == balance2.amount

    @pytest.mark.asyncio
    async def test_transfer_with_memo_and_fee_rate(self):
        self.client = Client(self.phrase_for_tx1, network='testnet')
        fee_rates = await self.client.get_fee_rates()
        fee_rate = fee_rates['fast']
        balance = await self.client.get_balance()
        if balance.amount > 0:
            amount = 0.0000001
            tx_id = await self.client.transfer(amount, self.testnetaddress_for_tx2, self.memo, fee_rate)
            assert tx_id
        self.client.purge_client()

    @pytest.mark.asyncio
    async def test_purge_client_should_purge_phrase_and_utxos(self):
        self.client = Client(self.phrase, network='testnet')
        self.client.purge_client()
        with pytest.raises(Exception) as err:
            self.client.get_address()
        assert str(err.value) == "Phrase must be provided"
        with pytest.raises(Exception) as err:
            await self.client.get_balance()
        assert str(err.value) == "Phrase must be provided"

    @pytest.mark.asyncio
    async def test_should_prevent_tx_when_fees_and_valueOut_exceed_balance(self, client):
        balance = await self.client.get_balance()
        if balance.amount > 0:
            amount = balance.amount + 1000  # BTC
            with pytest.raises(Exception) as err:
                await self.client.transfer(amount, self.testnetaddress_for_tx2)
            assert str(err.value) == "Balance insufficient for transaction"

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
    async def test_normal_tx_fees_and_vault_tx_fees(self, client):
        normal_tx = await self.client.get_fees()
        vault_tx = await self.client.get_fees_with_memo(self.memo)

        if vault_tx['average'] > MIN_TX_FEE:
            assert vault_tx['average'] > normal_tx['average']
        else:
            assert vault_tx['average'] == MIN_TX_FEE

    @pytest.mark.asyncio
    async def test_different_fees_normal_tx(self, client):
        fees = await self.client.get_fees()

        assert fees['fastest'] > fees['fast']
        assert fees['fast'] > fees['average']

    @pytest.mark.asyncio
    async def test_has_balances_invalid_address(self, client):
        with pytest.raises(Exception) as err:
            await self.client.get_balance(address='invalid address')
        assert str(err.value) == "Invalid Address"

    @pytest.mark.asyncio
    async def test_transfer_invalid_address(self, client):
        balance = await self.client.get_balance()
        if balance.amount > 0:
            amount = 0.0000001
            with pytest.raises(Exception) as err:
                await self.client.transfer(amount, 'invalid address')
            assert str(err.value) == "Invalid address"

    @pytest.mark.asyncio
    async def test_get_transactions(self, client):
        txs = await self.client.get_transactions({'address': self.address_for_transactions, 'limit': 4})
        assert txs
        if txs['total'] > 0:
            tx = txs['tx'][0]
            assert tx.asset == self.btc_asset
            assert tx.tx_date
            assert tx.tx_hash
            assert tx.tx_type == 'transfer'
            assert len(tx.tx_to)
            assert len(tx.tx_from)

    @pytest.mark.asyncio
    async def test_get_transactions_limit_should_work(self, client):
        txs = await self.client.get_transactions({'address': self.address_for_transactions, 'limit': 1})
        assert len(txs['tx']) == 1    

    @pytest.mark.asyncio
    async def test_get_transaction_with_hash(self, client):
        tx_data = await self.client.get_transaction_data('b660ee07167cfa32681e2623f3a29dc64a089cabd9a3a07dd17f9028ac956eb8')
        assert tx_data.tx_hash == 'b660ee07167cfa32681e2623f3a29dc64a089cabd9a3a07dd17f9028ac956eb8'
        assert len(tx_data.tx_from) == 1
        assert tx_data.tx_from[0].address == '2N4nhhJpjauDekVUVgA1T51M5gVg4vzLzNC'
        assert tx_data.tx_from[0].amount == '0.08898697'

        assert len(tx_data.tx_to) == 2
        assert tx_data.tx_to[0].address == 'tb1q3a00snh7erczk94k48fe9q5z0fldgnh4twsh29'
        assert tx_data.tx_to[0].amount == '0.00100000'

        assert tx_data.tx_to[1].address == 'tb1qxx4azx0lw4tc6ylurc55ak5hl7u2ws0w9kw9h3'
        assert tx_data.tx_to[1].amount == '0.08798533'