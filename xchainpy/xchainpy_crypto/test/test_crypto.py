from Crypto.Cipher import AES
import pytest
from xchainpy.xchainpy_crypto import crypto


class TestCrypto:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    phrase2 = 'flush viable fury sword mention dignity ethics secret nasty gallery teach fever'
    def test_valid_phrase(self):
        assert crypto.validate_phrase(self.phrase) == True

    def test_invalid_phrase(self):
        assert crypto.validate_phrase('invalid phrase') == False

    def test_export_keystore(self):
        password = 'thorchain'
        keystore = crypto.encrypt_to_keystore(self.phrase , password)
        assert keystore.crypto.cipher == AES.MODE_CTR
        assert keystore.crypto.kdf == 'pbkdf2'
        assert keystore.crypto.kdf_params.prf == 'hmac-sha256'
        assert keystore.crypto.kdf_params.c == 262144
        assert keystore.version == 1
        assert keystore.meta == 'xchain-keystore'
    
    def test_import_keystore(self):
        password = 'thorchain'
        keystore = crypto.encrypt_to_keystore(self.phrase2 , password)
        decrypted = crypto.decrypt_from_keystore(keystore , password)
        assert decrypted == self.phrase2

