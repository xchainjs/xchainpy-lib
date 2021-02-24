import pytest
from xchainpy.xchainpy_bitcoincash import utils

class TestBitcoinCashUtils:
    memo = 'SWAP:THOR.RUNE'

    def test_get_right_vault_fee(self):
        assert utils.calc_fee(fee_rate=10, memo=self.memo) == 1030

    def test_get_normal_fee(self):
        assert utils.calc_fee(fee_rate=10) == 780