import pytest
from xchainpy.xchainpy_litecoin.client import Client
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_litecoin.utils import MIN_TX_FEE

class TestLiteCoinClient:

    phrase = 'atom green various power must another rent imitate gadget creek fat then'
    phrase_one = 'atom green various power must another rent imitate gadget creek fat then'
    testnetaddress = 'tltc1q2pkall6rf6v6j0cvpady05xhy37erndv05de7g'
    ltc_asset = Asset('LTC', 'LTC')
    memo = 'SWAP:THOR.RUNE' 

    # phraseTwo = 'green atom various power must another rent imitate gadget creek fat then'
    address_two = 'tltc1ql68zjjdjx37499luueaw09avednqtge4u23q36'

    # Third ones is used only for balance verification
    phrase_three = 'quantum vehicle print stairs canvas kid erode grass baby orbit lake remove'
    address_three = 'tltc1q04y2lnt0ausy07vq9dg5w2rnn9yjl3rz364adu'

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
    async def test_transfer_with_memo_and_fee_rate(self, client):
        fee_rates = await self.client.get_fee_rates()
        fee_rate = fee_rates['fast']
        balance = await self.client.get_balance()
        if balance.amount > 0:
            amount = 0.0000001
            tx_id = await self.client.transfer(amount, self.address_two, self.memo, fee_rate)
            assert tx_id

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
            amount = balance.amount + 1000  # LTC
            with pytest.raises(Exception) as err:
                await self.client.transfer(amount, self.address_two)
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
        txs = await self.client.get_transactions({'address': self.address_three, 'limit': 4})
        assert txs
        if txs['total'] > 0:
            tx = txs['tx'][0]
            assert tx.asset == self.ltc_asset
            assert tx.tx_date
            assert tx.tx_hash
            assert tx.tx_type == 'transfer'
            assert len(tx.tx_to)
            assert len(tx.tx_from)

    @pytest.mark.asyncio
    async def test_get_transactions_limit_should_work(self, client):
        txs = await self.client.get_transactions({'address': self.address_three, 'limit': 1})
        assert len(txs['tx']) == 1    

    @pytest.mark.asyncio
    async def test_get_transaction_with_hash(self, client):
        tx_data = await self.client.get_transaction_data('b0422e9a4222f0f2b030088ee5ccd33ac0d3c59e7178bf3f4626de71b0e376d3')
        assert tx_data.tx_hash == 'b0422e9a4222f0f2b030088ee5ccd33ac0d3c59e7178bf3f4626de71b0e376d3'
        assert len(tx_data.tx_from) == 1
        assert tx_data.tx_from[0].address == 'tltc1q2pkall6rf6v6j0cvpady05xhy37erndv05de7g'
        assert tx_data.tx_from[0].amount == '8.60368562'

        assert len(tx_data.tx_to) == 2
        assert tx_data.tx_to[0].address == 'tltc1q04y2lnt0ausy07vq9dg5w2rnn9yjl3rz364adu'
        assert tx_data.tx_to[0].amount == '0.00002223'

        assert tx_data.tx_to[1].address == 'tltc1q2pkall6rf6v6j0cvpady05xhy37erndv05de7g'
        assert tx_data.tx_to[1].amount == '8.60365339'