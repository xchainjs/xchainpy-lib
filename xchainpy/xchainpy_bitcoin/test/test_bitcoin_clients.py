import pytest
from xchainpy.xchainpy_bitcoin.client import Client
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models import tx_types

class TestBitcoinClient:

    # please don't touch the tBTC in these
    phrase = 'atom green various power must another rent imitate gadget creek fat then'
    testnetaddress = 'tb1q2pkall6rf6v6j0cvpady05xhy37erndvku08wp'
    btc_asset = Asset('BTC', 'BTC')

    phraseForTX = 'radar napkin latin present crumble peace dinner pool liar asset orphan coral'
    testnetaddressForTx = 'tb1q4x4aenx0gqgh6zrujr9nhrjpltywet4r0s2nky'
    
    transfer_amount = 0.00001
    single_tx_fee = 37500
    multi_tx_fee = 30000
    transfer_fee = {'average': single_tx_fee, 'fast': single_tx_fee, 'fastest': single_tx_fee }
    multi_send_fee = {'average': multi_tx_fee, 'fast': multi_tx_fee, 'fastest': multi_tx_fee }


    @pytest.fixture
    def client(self):
        self.client = Client(self.phrase, network='testnet')
        yield
        self.client.purge_client()

    def test_right_address(self, client):
        assert self.client.get_address() == self.testnetaddress

    def test_invalid_phrase(self):
        with pytest.raises(Exception) as err:
            assert Client(phrase= 'Invalid Phrase')
        assert str(err.value) == "Invalid Phrase"

    def test_right_phrase(self, client):
        assert self.client.set_phrase(self.phraseForTX) == self.testnetaddressForTx

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        assert await self.client.get_balance()

    # @pytest.mark.asyncio
    # async def test_has_no_balances(self, client):
    #     self.client.set_network('mainnet')
    #     assert await self.client.get_balance() == []