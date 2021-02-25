import pytest
from xchainpy.xchainpy_litecoin.client import Client
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models import tx_types


class TestLiteCoinClient:

    # please don't touch the tBTC in these
    phrase = 'atom green various power must another rent imitate gadget creek fat then'
    phrase_one = 'atom green various power must another rent imitate gadget creek fat then'
    addy_one = 'tltc1q2pkall6rf6v6j0cvpady05xhy37erndv05de7g'
    ltc_asset = Asset('LTC', 'LTC')
    memo = 'SWAP:THOR.RUNE' 

    addyTwo = 'tltc1ql68zjjdjx37499luueaw09avednqtge4u23q36'

    phraseThree = 'quantum vehicle print stairs canvas kid erode grass baby orbit lake remove'
    addyThree = 'tltc1q04y2lnt0ausy07vq9dg5w2rnn9yjl3rz364adu'

    @pytest.fixture
    def client(self):
        self.client = Client(self.phrase, network='testnet')
        yield
        self.client.purge_client()
