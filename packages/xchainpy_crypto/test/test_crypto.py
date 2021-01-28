import pytest
from xchainpy_crypto import crypto


class TestCrypto:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'

    def test_valid_phrase(self):
        assert crypto.validate_phrase(self.phrase) == True

    def test_invalid_phrase(self):
        assert crypto.validate_phrase('invalid phrase') == False