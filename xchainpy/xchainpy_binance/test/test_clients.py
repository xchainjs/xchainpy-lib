import pytest
from xchainpy.xchainpy_binance.clients import Client
from xchainpy.xchainpy_util.asset import Asset

class TestClient:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    mainnetaddress = 'bnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9e738vr'
    testnetaddress = 'tbnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9htcrvj'
    bnb_asset = Asset('BNB', 'BNB', 'BNB')

    phraseForTX = 'wheel leg dune emerge sudden badge rough shine convince poet doll kiwi sleep labor hello'
    testnetaddressForTx = 'tbnb1t95kjgmjc045l2a728z02textadd98yt339jk7'
    
    transfer_amount = 0.001
    single_tx_fee = 37500

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

    @pytest.mark.asyncio
    async def test_should_broadcast_transfer(self, client):
        client.set_network('testnet')
        client.set_phrase(self.phraseForTX)
        assert client.get_address() == self.testnetaddressForTx
        before_balance = await client.get_balance()
        before_balance_amount = before_balance[0].amount
        assert len(before_balance) == 1
        await client.transfer(asset=self.bnb_asset, amount=self.transfer_amount, recipient=self.testnetaddressForTx)
        after_balance = await client.get_balance()
        after_balance_amount = after_balance[0].amount
        assert round((float(before_balance_amount) - float(after_balance_amount)) * 10**8) == self.single_tx_fee