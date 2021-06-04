from typing import Counter
from .models.Keystore import Keystore
from .models.KdfParams import KdfParams
from bip_utils import Bip39MnemonicValidator
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Hash import BLAKE2b
from Crypto.Cipher import AES
from Crypto.Util import Counter
from .models.CryptoStruct import CryptoStruct
from .models.CipherParams import CipherParams
from . import utils
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
    is_valid = Bip39MnemonicValidator(phrase).IsValid()
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

    kdfparams = KdfParams(prf=PRF, dklen=DKLEN, salt=salt.hex(), c=C)

    ciptherparams = CipherParams(iv.hex())


    derived_key = await utils.pbkdf2(
        password, salt, kdfparams.c, kdfparams.dklen, HASHFUNCTION
    )

    ctr = Counter.new(NBITS, initial_value=int(iv.hex(), 16))
    aes_cipher = AES.new(derived_key[0:16], AES.MODE_CTR, counter=ctr)
    cipherbytes = aes_cipher.encrypt(phrase.encode("utf8"))

    blake256 = BLAKE2b.new(digest_bits=256)
    blake256.update((derived_key[16:32] + cipherbytes))
    mac = blake256.hexdigest()

    crypto_struct = CryptoStruct("aes-128-ctr" , cipherbytes.hex() , ciptherparams ,KDF, kdfparams, mac)

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
    if not isinstance(keystore, Keystore):
        keystore = Keystore.from_dict(keystore)

    kdfparams = keystore.crypto.kdfparams
    try:
        derived_key = await utils.pbkdf2(
            password,
            bytes.fromhex(kdfparams.salt),
            kdfparams.c,
            kdfparams.dklen,
            HASHFUNCTION,
        )

        cipherbytes = bytes.fromhex(keystore.crypto.ciphertext)

        blake256 = BLAKE2b.new(digest_bits=256)
        blake256.update((derived_key[16:32] + cipherbytes))
        mac = blake256.hexdigest()

        if mac != keystore.crypto.mac:
            raise Exception("Invalid Password")

        ctr = Counter.new(
            NBITS, initial_value=int(keystore.crypto.cipherparams.iv, 16)
        )
        aes_decipher = AES.new(
            derived_key[0:16], AES.MODE_CTR, counter=ctr
        )

        decipher_bytes = aes_decipher.decrypt(cipherbytes)

        res = bytes.decode(decipher_bytes)
        return res

    except Exception as err:
        raise Exception(err)
