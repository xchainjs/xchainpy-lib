import pytest
from xchainpy_litecoin.models.client_types import LitecoinClientParams, LitecoinTxParams
from xchainpy_litecoin.client import Client
from xchainpy_litecoin.const import MIN_TX_FEE
from xchainpy_client.models.types import Network
from xchainpy_client.models import tx_types
from xchainpy_util.asset import AssetLTC



class TestBitcoinClient:

    # please don't touch the tBTC in these
    phrase_one = 'atom green various power must another rent imitate gadget creek fat then'
    # m/84'/1'/0'/0/0
    phrase_one_testnet_address_path0 = 'tltc1q2pkall6rf6v6j0cvpady05xhy37erndv05de7g'
    # m/84'/1'/0'/0/1
    phrase_one_testnet_address_path1 = 'tltc1qut59ufcscqnkp8fgac68pj2ps5dzjjg4eggfqd'
    # m/84'/2'/0'/0/0
    phrase_one_mainnet_address_path0 = 'ltc1qll0eutk38yy3jms0c85v4ey68z83c78h3fmsh3'
    # m/84'/2'/0'/0/1
    phrase_one_mainnet_address_path1 = 'ltc1qsr5wh2sudyc7axh087lg7py6dsagphef63acgq'


    phrase_two = 'quantum vehicle print stairs canvas kid erode grass baby orbit lake remove'
    # m/84'/1'/0'/0/0
    phrase_two_testnet_address_path0 = 'tltc1q04y2lnt0ausy07vq9dg5w2rnn9yjl3rz364adu'

    memo = 'SWAP:THOR.RUNE'

    @pytest.fixture
    def client(self):
        self.client = Client(LitecoinClientParams(network='mainnet'))
        yield
        self.client.purge_client()

    def test_set_phrase_right_address(self, client):
        self.client.set_network('testnet')
        address = self.client.set_phrase(self.phrase_one)
        assert address == self.phrase_one_testnet_address_path0

    def test_invalid_phrase(self, client):
        with pytest.raises(Exception) as err:
            assert self.client.set_phrase('Invalid phrase')
        assert str(err.value) == "invalid phrase"

    def test_validate_address(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)
        assert self.client.validate_address(
            network=self.client.network, address=self.phrase_one_testnet_address_path0)

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_two)
        balance = await self.client.get_balance(address=self.client.get_address())
        balance = balance[0]
        assert balance.amount

    @pytest.mark.asyncio
    async def test_has_no_balances(self, client):
        self.client.set_phrase(self.phrase_two)
        balance = await self.client.get_balance(address=self.client.get_address())
        balance = balance[0]
        assert balance.amount == 0

    @pytest.mark.asyncio
    async def test_equal_balances_when_call_getbalance_twice(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_two)
        balance1 = await self.client.get_balance(address=self.client.get_address())
        balance1 = balance1[0]
        balance2 = await self.client.get_balance(address=self.client.get_address())
        balance2 = balance2[0]
        assert balance1.amount == balance2.amount

    @pytest.mark.asyncio
    async def test_transfer_invalid_address(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)
        amount = 0.0000001
        with pytest.raises(Exception) as err:
            await self.client.transfer(LitecoinTxParams(amount, 'invalid address'))
        assert str(err.value) == "Invalid address"

    @pytest.mark.asyncio
    async def test_should_prevent_tx_when_fees_and_valueOut_exceed_balance(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)
        balance = await self.client.get_balance(self.client.get_address())
        balance = balance[0]
        if balance.amount > 0:
            amount = balance.amount + 1000  # BTC
            with pytest.raises(Exception) as err:
                await self.client.transfer(LitecoinTxParams(amount, self.phrase_one_testnet_address_path0))
            assert str(err.value) == "Balance insufficient for transaction"

    @pytest.mark.asyncio
    async def test_transfer_with_memo_and_fee_rate(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)

        fee_rates = await self.client.get_fee_rates()
        fee_rate = fee_rates.fast
        balance = await self.client.get_balance(address=self.client.get_address())
        balance = balance[0]
        if balance.amount > 0:
            amount = 0.0000001
            tx_id = await self.client.transfer(LitecoinTxParams(amount, self.phrase_one_testnet_address_path0, self.memo, fee_rate))
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
    async def test_normal_tx_fees_and_vault_tx_fees(self, client):
        normal_tx = await self.client.get_fees()
        vault_tx = await self.client.get_fees(self.memo)

        if vault_tx.average > MIN_TX_FEE:
            assert vault_tx.average > normal_tx.average
        else:
            assert vault_tx.average == MIN_TX_FEE

    @pytest.mark.asyncio
    async def test_different_fees_normal_tx(self, client):
        fees = await self.client.get_fees()

        assert fees.fastest > fees.fast
        assert fees.fast > fees.average

    @pytest.mark.asyncio
    async def test_has_balances_invalid_address(self, client):
        with pytest.raises(Exception) as err:
            await self.client.get_balance(address='invalid address')
        assert str(err.value) == "Invalid Address"

    @pytest.mark.asyncio
    async def test_get_transactions(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)
        txs = await self.client.get_transactions(tx_types.TxHistoryParams(address=self.client.get_address(), limit=4))
        assert txs
        if txs.total > 0:
            tx = txs.txs[0]
            assert tx.asset == AssetLTC
            assert tx.tx_date
            assert tx.tx_hash
            assert tx.tx_type == 'transfer'
            assert len(tx.tx_to)
            assert len(tx.tx_from)

    @pytest.mark.asyncio
    async def test_get_transactions_limit_should_work(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)
        txs = await self.client.get_transactions(tx_types.TxHistoryParams(address=self.client.get_address(), limit=1))
        assert len(txs.txs) == 1

    @pytest.mark.asyncio
    async def test_get_transaction_with_hash(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_one)
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

    def test_should_return_valid_explorer_url(self, client):
        assert self.client.get_explorer_url() == 'https://ltc.bitaps.com'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_url() == 'https://tltc.bitaps.com'

    def test_should_retrun_valid_explorer_address_url(self, client):
        assert self.client.get_explorer_address_url('anotherTestAddressHere') == 'https://ltc.bitaps.com/anotherTestAddressHere'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_address_url('testAddressHere') == 'https://tltc.bitaps.com/testAddressHere'

    def test_should_retrun_valid_explorer_tx_url(self, client):
        assert self.client.get_explorer_tx_url('anotherTestTxHere') == 'https://ltc.bitaps.com/anotherTestTxHere'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_tx_url('testTxHere') == 'https://tltc.bitaps.com/testTxHere'

    def test_should_derivate_the_address_correctly(self, client):
        self.client.set_phrase(self.phrase_one)
        self.client.set_network('testnet')
        assert self.client.get_address(index=0) == self.phrase_one_testnet_address_path0
        assert self.client.get_address(index=1) == self.phrase_one_testnet_address_path1

        self.client.set_network('mainnet')
        assert self.client.get_address(index=0) == self.phrase_one_mainnet_address_path0
        assert self.client.get_address(index=1) == self.phrase_one_mainnet_address_path1

    @pytest.mark.asyncio
    async def test_purge_client_should_purge_phrase_and_utxos(self):
        self.client = Client(LitecoinClientParams(network='testnet', phrase=self.phrase_one))
        self.client.purge_client()
        with pytest.raises(Exception) as err:
            self.client.get_address()
        assert str(err.value) == "Phrase must be provided"