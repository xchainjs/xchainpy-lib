import pytest
from xchainpy_util import chain

class TestChain:

    def test_is_chain(self):
        assert chain.is_chain('BNB')

    def test_invalid_chain(self):
        assert not chain.is_chain('invalid chain')