from bip_utils import Bip39MnemonicValidator
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Hash import BLAKE2b
from Crypto.Cipher import AES
import xchainpy.xchainpy_crypto.utils as utils
import uuid

CIPHER = AES.MODE_CTR
KDF = 'pbkdf2'
PRF = 'hmac-sha256'
DKLEN = 32
C = 262144
HASHFUNCTION = SHA256
META = 'xchain-keystore'


# Validate a mnemonic string by verifying its checksum
def validate_phrase(phrase: str):
    """Check validity of mnemonic (phrase)

    :param phrase: a phrase
    :type phrase: str
    :returns: is the phrase valid or not (true or false)
    """
    is_valid = Bip39MnemonicValidator(phrase).Validate()
    return is_valid


#TODO: must be async
def encrypt_to_keystore(phrase: str, password: str):
    if not validate_phrase(phrase):
        raise Exception("Invalid BIP39 Phrase")

    ID = uuid.uuid4()
    salt = get_random_bytes(32)
    iv = get_random_bytes(16)

    kdf_params = {"prf": PRF, "dklen": DKLEN, "salt": salt.hex(), "c": C}
    cipther_params = {"iv": iv.hex()}

    derived_key = utils.pbkdf2(
        password, salt, kdf_params['c'], kdf_params['dklen'], HASHFUNCTION)
    aes_cipher = AES.new(derived_key[0:16], CIPHER, iv)
    cipher_bytes = aes_cipher.encrypt(phrase)
    blake256 = BLAKE2b.new(digest_bits=256)
    blake256.update((derived_key[16:32] + cipher_bytes))
    mac = blake256.hexdigest()

    crypto_struct = {"cipher": CIPHER, "cipher_text": cipher_bytes.hex()
    , "cipher_params": cipther_params, "kdf": KDF, "kdf_params": kdf_params, "mac": mac}

    keystore = {
        "crypto" : crypto_struct,
        "id" : ID,
        "version" : 1,
        "mata" : META
    }

    return keystore

#TODO: must be async
def decrypt_from_keystore(keystore , password : str):
    kdf_params = keystore['crypto']['kdf_params']
    try:
        derived_key = utils.pbkdf2(password ,bytes.fromhex(kdf_params['salt']),kdf_params['c'],kdf_params['dklen'],HASHFUNCTION)

        cipher_bytes = bytes.fromhex(keystore['crypto']['cipher_text'])
        
        blake256 = BLAKE2b.new(digest_bits=256)
        blake256.update((derived_key[16:32] + cipher_bytes))
        mac = blake256.hexdigest()

        if mac != keystore['crypto']['mac'] :
            raise Exception('Invalid Password')

        aes_decipher = AES.new(derived_key[0:16],keystore['crypto']['cipher'],bytes.fromhex(keystore['crypto']['cipher_params']['iv']))
        decipher_bytes = aes_decipher.decrypt(cipher_bytes)

        res = bytes.decode(decipher_bytes)
        return res;
        

    except Exception as err:
        raise Exception(err)