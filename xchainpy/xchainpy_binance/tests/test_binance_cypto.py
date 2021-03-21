import pytest
from xchainpy_binance import crypto

class TestBinanceCrypto:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    seed = b'\xd0s%ch\xc9W\xfc)\x0f_\x9d&5\xe3\xe0u\xd4\xe2\x80\xc4\x81C\xef"\xc7g\xba-\xa2"\xa9\x89\xe9\xe4\xc2\xa3\x87\x08\xdfa\xb7\x17!\x1b\xefD\xd8C\xe3@\xe8~C\xe0p\xc1\x83\xd8V~\xa6\x8ee'
    private_key = 'f995100f54f43f8e7b5e4e64ccc797df7d05db16ee76a39df38d5d5f2c526226'
    public_key = b'\x03>\x98\xf7\xfd\xc3\x0c\x89r&\xec\xd1\x05\xc6\xe4\xe6i\xbb\xe9-L\x83O\x0b\x84\x04\xe7\xea\xd6\x156\x16\xbc'
    testnetaddress = 'tbnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9htcrvj'

    def test_mnemonic_to_seed(self):
        assert crypto.mnemonic_to_seed(self.phrase) == self.seed

    def test_mnemonic_to_private_key(self):
        assert crypto.mnemonic_to_private_key(self.phrase) == self.private_key

    def test_private_key_to_public_key(self):
        assert crypto.private_key_to_public_key(self.private_key) == self.public_key

    def test_private_key_to_address(self):
        assert crypto.private_key_to_address(self.private_key, 'tbnb') == self.testnetaddress

    def test_public_key_to_address(self):
        assert crypto.public_key_to_address(self.public_key, 'tbnb')

    def test_check_address(self):
        assert crypto.check_address(self.testnetaddress, 'tbnb') == True

    def test_check_address_false_address(self):
        assert crypto.check_address(self.testnetaddress + '1', 'tbnb') == False

    def test_check_address_false_prefix(self):
        assert crypto.check_address(self.testnetaddress, 'bnb') == False