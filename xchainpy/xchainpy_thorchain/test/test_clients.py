import pytest

from xchainpy.xchainpy_thorchain.client import Client
from xchainpy.xchainpy_binance.models.coin import Coin
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models import tx_types

class TestClient:

    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    mainnetaddress = 'thor19kacmmyuf2ysyvq3t9nrl9495l5cvktjs0yfws'
    testnetaddress = 'tthor19kacmmyuf2ysyvq3t9nrl9495l5cvktj5c4eh4'
    rune_asset = Asset('THOR', 'RUNE', 'RUNE')

    phraseForTX = 'history dice polar glad split follow tired invest lemon mask all industry'
    testnetaddressForTx = 'tthor103nyx8erew2tc5knfcj7se5hsvvmr4ew7fpn4t'
    testnetTransfer = 'tthor1pttyuys2muhj674xpr9vutsqcxj9hepy4ddueq'

    sampleTX = '8A2EC1EE711D1057594FAA9F7F82B6E0D726745F4E88372F6FFACC38C36D234B'

    transfer_amount = 0.01
    single_tx_fee = 10000000
    transfer_fee = {'average': single_tx_fee, 'fast': single_tx_fee, 'fastest': single_tx_fee }

    @pytest.fixture
    def client(self):
        self.client = Client(self.phrase, network='mainnet')
        yield
        self.client.purge_client()

    def test_empty_wallet_main(self):
        client = Client(self.phrase, network= 'mainnet')
        address_main = client.get_address()
        assert address_main == self.mainnetaddress

    def test_empty_wallet_test(self):
        client = Client(self.phrase, network= 'testnet')
        address_test = client.get_address()
        assert address_test == self.testnetaddress

    def test_invalid_phrase(self):
        with pytest.raises(Exception) as err:
            assert Client(phrase= 'invalid phrase')
        assert str(err.value) == "invalid phrase"

    def test_right_address(self, client):
        assert self.client.get_address() == self.mainnetaddress

    def test_update_net(self, client):
        self.client.set_network('testnet')
        assert self.client.get_network() == 'testnet'
        assert self.client.get_address() == self.testnetaddress
    
    def test_set_phrase_return_address(self, client):
        assert self.client.set_phrase(self.phrase) == self.mainnetaddress
        self.client.set_network('testnet')
        assert self.client.set_phrase(self.phrase) == self.testnetaddress

    @pytest.mark.asyncio
    async def test_has_no_balances(self, client):
        assert await self.client.get_balance() == []

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        self.client.set_network('testnet')
        assert await self.client.get_balance()

    @pytest.mark.asyncio
    async def test_balance_has_correct_asset(self, client):
        self.client.set_network('testnet')
        balance = await self.client.get_balance(self.testnetaddress)
        assert 'THOR.' + str(balance[0]['asset']).upper() == str(self.rune_asset)
        assert balance[0]['amount'] == '0.9799'

    @pytest.mark.asyncio
    async def test_should_broadcast_transfer(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phraseForTX)
        assert self.client.get_address() == self.testnetaddressForTx
        before_balance = await self.client.get_balance()
        assert len(before_balance) == 1
        before_balance_amount = before_balance[0]['amount']
        print(before_balance_amount)
        await self.client.transfer(amount=self.transfer_amount, recipient=self.testnetTransfer, asset=self.rune_asset)
        after_balance = await self.client.get_balance()
        after_balance_amount = after_balance[0]['amount']
        assert round((float(before_balance_amount) - float(after_balance_amount)) * 10**8) == 3000000

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_input_amount_higher_than_balance(self , client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phraseForTX)
        before_balance = await self.client.get_balance()
        before_balance_amount = before_balance[0]['amount']
        send_amount = float(before_balance_amount) + 1
        with pytest.raises(Exception) as err:
            assert await self.client.transfer(amount=send_amount, recipient=self.testnetaddressForTx, asset=self.rune_asset)
        assert str(err.value) == "input asset amout is higher than current (asset balance - transfer fee)"

    @pytest.mark.asyncio
    async def test_get_transfer_fees(self, client):
        self.client.set_network('testnet')
        fee = await self.client.get_fees()
        assert fee['average'] == str(self.transfer_fee['average'])
        assert fee['fast'] == str(self.transfer_fee['fast'])
        assert fee['fastest'] == str(self.transfer_fee['fastest'])

    def test_validate_address(self, client):
        assert self.client.validate_address(self.testnetaddress, 'tthor') == True

    def test_validate_address_false_address(self, client):
        assert self.client.validate_address(self.testnetaddress + '1', 'tthor') == False

    def test_validate_address_false_prefix(self, client):
        assert self.client.validate_address(self.testnetaddress, 'thor') == False

    @pytest.mark.asyncio
    async def test_get_transaction_data(self, client):
        self.client.set_network('testnet')
        try:
            transaction = await self.client.get_transaction_data(self.sampleTX)
            assert transaction
        except Exception as err:
            assert str(err) == 'transaction not found' # no transaction found