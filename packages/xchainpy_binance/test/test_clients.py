import pytest
from xchainpy_binance.clients import Client
from xchainpy_util.asset import Asset

class TestClient:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    mainnetaddress = 'bnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9e738vr'
    testnetaddress = 'tbnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9htcrvj'
    bnb_asset = Asset('BNB', 'BNB', 'BNB')

    @pytest.fixture
    def client(self):
        return Client(self.phrase, network='mainnet')

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
        assert client.get_address() == self.mainnetaddress

    def test_update_net(self, client):
        client.set_network('testnet')
        assert client.get_network() == 'testnet'
        assert client.get_address() == self.testnetaddress
    
    def test_set_phrase_return_address(self, client):
        assert client.set_phrase(self.phrase) == self.mainnetaddress
        client.set_network('testnet')
        assert client.set_phrase(self.phrase) == self.testnetaddress

    @pytest.mark.asyncio
    async def test_has_no_balances(self, client):
        assert await client.get_balance() == []

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        client.set_network('testnet')
        assert await client.get_balance()

    @pytest.mark.asyncio
    async def test_balance_has_correct_asset(self, client):
        client.set_network('testnet')
        balance = await client.get_balance(self.testnetaddress, self.bnb_asset)
        assert str(balance[0].asset) == str(self.bnb_asset)
        assert balance[0].amount == '12.92899000'