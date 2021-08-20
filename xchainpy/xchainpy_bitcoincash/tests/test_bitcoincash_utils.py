import pytest
from xchainpy_bitcoincash import utils

class TestBitcoinCashUtils:
    memo = 'SWAP:THOR.RUNE'
    testnet_address = 'bchtest:qpd7jmj0hltgxux06v9d9u6933vq7zd0kyjlapya0g'
    mainnet_address = 'bitcoincash:qp4kjpk684c3d9qjk5a37vl2xn86wxl0f5j2ru0daj'


    def test_get_right_vault_fee(self):
        assert utils.calc_fee(fee_rate=10, memo=self.memo) == 1030

    def test_get_normal_fee(self):
        assert utils.calc_fee(fee_rate=10) == 780