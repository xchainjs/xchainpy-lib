import pytest
from xchainpy_binance.clients import Client

class TestClient:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    mainnetaddress = 'bnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9e738vr'
    testnetaddress = 'tbnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9htcrvj'

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