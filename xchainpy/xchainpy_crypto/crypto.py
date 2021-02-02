from typing import Counter
from xchainpy.xchainpy_crypto.models.Keystore import Keystore
from xchainpy.xchainpy_crypto.models.KdfParams import KdfParams
from bip_utils import Bip39MnemonicValidator
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Hash import BLAKE2b
from Crypto.Cipher import AES
from Crypto.Util import Counter
from xchainpy.xchainpy_crypto.models.CryptoStruct import CryptoStruct
from xchainpy.xchainpy_crypto.models.CipherParams import CipherParams
import xchainpy.xchainpy_crypto.utils as utils
import uuid

CIPHER = AES.MODE_CTR
NBITS = 128
KDF = "pbkdf2"
PRF = "hmac-sha256"
DKLEN = 32
C = 262144
HASHFUNCTION = SHA256
META = "xchain-keystore"


def validate_phrase(phrase: str):
    """Check validity of mnemonic (phrase)

    Validate a mnemonic string by verifying its checksum
    :param phrase: a phrase
    :type phrase: str
    :returns: is the phrase valid or not (true or false)
    """
    is_valid = Bip39MnemonicValidator(phrase).Validate()
    return is_valid


async def encrypt_to_keystore(phrase: str, password: str):
    """Get the Keystore from the given phrase and password.

    Args:
        phrase (str): phrase
        password (str): password

    Raises:
        Exception: if phrase is invalid

    Returns:
        [type]: Keystore
    """
    if not validate_phrase(phrase):
        raise Exception("Invalid BIP39 Phrase")

    ID = str(uuid.uuid4())
    salt = get_random_bytes(32)
    iv = get_random_bytes(16)

    kdf_params = KdfParams(prf=PRF , dklen=DKLEN , salt=salt.hex(),c=C)

    cipther_params = CipherParams(iv.hex())


    derived_key = await utils.pbkdf2(
        password, salt, kdf_params.c, kdf_params.dklen, HASHFUNCTION
    )

    ctr = Counter.new(NBITS, initial_value=int(iv.hex(), 16))
    aes_cipher = AES.new(derived_key[0:16], AES.MODE_CTR, counter=ctr)
    cipher_bytes = aes_cipher.encrypt(phrase.encode("utf8"))

    blake256 = BLAKE2b.new(digest_bits=256)
    blake256.update((derived_key[16:32] + cipher_bytes))
    mac = blake256.hexdigest()

    crypto_struct = CryptoStruct(CIPHER , cipher_bytes.hex() , cipther_params ,KDF,kdf_params,mac)

    keystore = Keystore(crypto_struct , ID, 1 , META)
    return keystore


async def decrypt_from_keystore(keystore : Keystore, password: str):
    """ Get the phrase from the keystore

    Args:
        keystore (Keystore): keystore
        password (str): password

    Raises:
        Exception: if password is incorrect
        Exception: any inner exceptions

    Returns:
        [type]: the phrase from keystore
    """
    kdf_params = keystore.crypto.kdf_params
    try:
        derived_key = await utils.pbkdf2(
            password,
            bytes.fromhex(kdf_params.salt),
            kdf_params.c,
            kdf_params.dklen,
            HASHFUNCTION,
        )

        cipher_bytes = bytes.fromhex(keystore.crypto.cipher_text)

        blake256 = BLAKE2b.new(digest_bits=256)
        blake256.update((derived_key[16:32] + cipher_bytes))
        mac = blake256.hexdigest()

        if mac != keystore.crypto.mac:
            raise Exception("Invalid Password")

        ctr = Counter.new(
            NBITS, initial_value=int(keystore.crypto.cipher_params.iv, 16)
        )
        aes_decipher = AES.new(
            derived_key[0:16], keystore.crypto.cipher, counter=ctr
        )

        decipher_bytes = aes_decipher.decrypt(cipher_bytes)

        res = bytes.decode(decipher_bytes)
        return res

    except Exception as err:
        raise Exception(err)