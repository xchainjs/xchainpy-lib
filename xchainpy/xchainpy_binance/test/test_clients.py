import pytest
from xchainpy.xchainpy_binance.client import Client
from xchainpy.xchainpy_util.asset import Asset

class TestClient:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    mainnetaddress = 'bnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9e738vr'
    testnetaddress = 'tbnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9htcrvj'
    bnb_asset = Asset('BNB', 'BNB', 'BNB')

    phraseForTX = 'wheel leg dune emerge sudden badge rough shine convince poet doll kiwi sleep labor hello'
    testnetaddressForTx = 'tbnb1t95kjgmjc045l2a728z02textadd98yt339jk7'
    
    transfer_amount = 0.0001
    single_tx_fee = 37500
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
        balance = await self.client.get_balance(self.testnetaddress, self.bnb_asset)
        assert str(balance[0].asset) == str(self.bnb_asset)
        assert balance[0].amount == '12.92899000'

    @pytest.mark.asyncio
    async def test_should_broadcast_transfer(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phraseForTX)
        assert self.client.get_address() == self.testnetaddressForTx
        before_balance = await self.client.get_balance()
        assert len(before_balance) == 1
        before_balance_amount = before_balance[0].amount
        await self.client.transfer(asset=self.bnb_asset, amount=self.transfer_amount, recipient=self.testnetaddressForTx)
        after_balance = await self.client.get_balance()
        after_balance_amount = after_balance[0].amount
        assert round((float(before_balance_amount) - float(after_balance_amount)) * 10**8) == self.single_tx_fee

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_input_amount_higher_than_balance(self , client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phraseForTX)
        before_balance = await self.client.get_balance()
        before_balance_amount = before_balance[0].amount
        send_amount = float(before_balance_amount) + 1
        with pytest.raises(Exception) as err:
            assert await self.client.transfer(asset=self.bnb_asset, amount=send_amount, recipient=self.testnetaddressForTx)
        assert str(err.value) == "input asset amout is higher than current (asset balance - transfer fee)"

    @pytest.mark.asyncio
    async def test_get_transfer_fees(self, client):
        self.client.set_network('testnet')
        fee = await self.client.get_fees()
        assert fee['average'] == self.transfer_fee['average'] * 10**-8
        assert fee['fast'] == self.transfer_fee['fast'] * 10**-8
        assert fee['fastest'] == self.transfer_fee['fastest'] * 10**-8