import pytest
from xchainpy_bitcoin.models.client_types import BitcoinClientParams, BitcinTxParams
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.const import *
from xchainpy_client.models.types import Network
from xchainpy_client.models import tx_types
from xchainpy_util.asset import AssetBTC


class TestBitcoinClient:

    # please don't touch the tBTC in these
    phrase_one = 'atom green various power must another rent imitate gadget creek fat then'
    # m/84'/1'/0'/0/0
    phrase_one_testnet_address_path0 = 'tb1q2pkall6rf6v6j0cvpady05xhy37erndvku08wp'
    # m/84'/1'/0'/0/1
    phrase_one_testnet_address_path1 = 'tb1qut59ufcscqnkp8fgac68pj2ps5dzjjg4qq2hsy'
    # m/84'/0'/0'/0/0
    phrase_one_mainnet_address_path0 = 'bc1qvdux5606j2zh5f4724wvnywe6gcj2tcrzz7wdl'
    # m/84'/0'/0'/0/1
    phrase_one_mainnet_address_path1 = 'bc1qnnkssp3sgfjjk2m0z9thjay0psp6ehlt6dzd97'


    phrase_two = 'quantum vehicle print stairs canvas kid erode grass baby orbit lake remove'
    # m/84'/0'/0'/0/0
    phrase_two_mainnet_address_path0 = 'bc1qsn4ujsja3ukdlzjmc9tcgpeaxeauq0ga83xmds'
    # m/84'/0'/0'/0/1
    phrase_two_mainnet_address_path1 = 'bc1q7c58pf87g73pk07ryq996jfa5nqkx2ppzjz8kq'


    phrase_for_tx1 = 'caution pear excite vicious exotic slow elite marble attend science strategy rude'
    testnet_address_for_tx1 = 'tb1qxe0e8793v3z0v0h2l3nglzg85k2jdx04vx088z'


    phrase_for_tx2 = 'theme neither sun invite illness chat project enough answer spray visual zoo'
    testnet_address_for_tx2 = 'tb1qymzatfxg22vg8adxlnxt3hkfmzl2rpuzpk8kcf'

    memo = 'SWAP:THOR.RUNE'

    @pytest.fixture
    def client(self):
        self.client = Client(BitcoinClientParams(network='mainnet', sochain_url='https://sochain.com/api/v2'))
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
        self.client.set_phrase(self.phrase_for_tx1)
        amount = 0.0000001
        with pytest.raises(Exception) as err:
            await self.client.transfer(BitcinTxParams(amount, 'invalid address'))
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
                await self.client.transfer(BitcinTxParams(amount, self.testnet_address_for_tx2))
            assert str(err.value) == "Balance insufficient for transaction"

    @pytest.mark.asyncio
    async def test_transfer_with_memo_and_fee_rate(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phrase_for_tx1)

        fee_rates = await self.client.get_fee_rates()
        fee_rate = fee_rates.fast
        balance = await self.client.get_balance(address=self.client.get_address())
        balance = balance[0]
        if balance.amount > 0:
            amount = 0.0000001
            tx_id = await self.client.transfer(BitcinTxParams(amount, self.testnet_address_for_tx2, self.memo, fee_rate))
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
            assert tx.asset == AssetBTC
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

    def test_should_return_valid_explorer_url(self, client):
        assert self.client.get_explorer_url() == 'https://blockstream.info'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_url() == 'https://blockstream.info/testnet'

    def test_should_retrun_valid_explorer_address_url(self, client):
        assert self.client.get_explorer_address_url('anotherTestAddressHere') == 'https://blockstream.info/address/anotherTestAddressHere'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_address_url('testAddressHere') == 'https://blockstream.info/testnet/address/testAddressHere'

    def test_should_retrun_valid_explorer_tx_url(self, client):
        assert self.client.get_explorer_tx_url('anotherTestTxHere') == 'https://blockstream.info/tx/anotherTestTxHere'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_tx_url('testTxHere') == 'https://blockstream.info/testnet/tx/testTxHere'

    def test_should_derivate_the_address_correctly(self, client):
        self.client.set_phrase(self.phrase_one)
        self.client.set_network('testnet')
        assert self.client.get_address(index=0) == self.phrase_one_testnet_address_path0
        assert self.client.get_address(index=1) == self.phrase_one_testnet_address_path1

        self.client.set_network('mainnet')
        assert self.client.get_address(index=0) == self.phrase_one_mainnet_address_path0
        assert self.client.get_address(index=1) == self.phrase_one_mainnet_address_path1

        self.client.set_phrase(self.phrase_two)
        assert self.client.get_address(index=0) == self.phrase_two_mainnet_address_path0
        assert self.client.get_address(index=1) == self.phrase_two_mainnet_address_path1

    @pytest.mark.asyncio
    async def test_purge_client_should_purge_phrase_and_utxos(self):
        self.client = Client(BitcoinClientParams(network='testnet', phrase=self.phrase_one))
        self.client.purge_client()
        with pytest.raises(Exception) as err:
            self.client.get_address()
        assert str(err.value) == "Phrase must be provided"