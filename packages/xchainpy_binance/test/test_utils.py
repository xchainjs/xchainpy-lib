import pytest
from xchainpy_binance import utils


class TestUtils:

    def test_get_prefix_testnet(self):
        assert utils.get_prefix('testnet') == 'tbnb'

    def test_get_prefix_mainnet(self):
        assert utils.get_prefix('mainnet') == 'bnb'