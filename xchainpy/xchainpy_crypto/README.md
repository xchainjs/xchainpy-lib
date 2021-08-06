# XCHAIN-CRYPTO

The XCHAIN CRYPTO package is a crypto package used by all `XCHAIN` clients.

XCHAIN-CRYPTO encrypts a master phrase to a keystore. This keystore can then be exported to other XCHAIN wallets or stored securely.

Users can export their phrase and import them into other wallets since it is a BIP39 compatible phrase.

## Design

Typically keystore files encrypt a `seed` to a file, however this is not appropriate or UX friendly, since the phrase cannot be recovered after the fact.

Crypto design:

[entropy] -> [phrase] -> [seed] -> [privateKey] -> [publicKey] -> [address]

Instead, XCHAIN-CRYPTO stores the phrase in a keystore file, then decrypts and passes this phrase to other clients:

[keystore] -> XCHAIN-CRYPTO -> [phrase] -> ChainClient

The ChainClients can then convert this into their respective key-pairs and addresses.
Users can also export their phrases after the fact, ensuring they have saved it securely. This could enhance UX onboarding since users aren't forced to write their phrases down immediately for empty or test wallets.

```python
# Crypto Constants for xchain
CIPHER = AES.MODE_CTR
NBITS = 128
KDF = "pbkdf2"
PRF = "hmac-sha256"
DKLEN = 32
C = 262144
HASHFUNCTION = SHA256
META = "xchain-keystore"
```

## Usage

### Basic usage

```python
from xchainpy_crypto.crypto import validate_phrase , encrypt_to_keystore , decrypt_from_keystore

isCorrect = validate_phrase(phrase)
password = 'thorchain'
keystore = await encrypt_to_keystore(phrase, password)
phraseDecrypted = await decrypt_from_keystore(keystore, password)
```

Keystore Model

```python
class Keystore:
    def __init__(self, crypto:CryptoStruct, id:str, version:int, meta:str):
        self._crypto = crypto
        self._id = id
        self._version = version
        self._meta = meta

    @classmethod
    def from_dict(cls, keystore):
        new_keystore = cls.__new__(cls)
        for key in keystore:
            setattr(new_keystore, key, keystore[key])
        return new_keystore

    @property
    def crypto(self):
        return self._crypto

    @crypto.setter
    def crypto(self, crypto):
        if isinstance(crypto, dict):
            self._crypto = CryptoStruct.from_dict(crypto)
        else:
            self._crypto = crypto

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def meta(self):
        return self._meta

    @meta.setter
    def meta(self, meta):
        self._meta = meta

    def to_json(self):
        return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()})
```

CipherParams

```python
class CipherParams:
    def __init__(self, iv:str):
        self._iv = iv

    @classmethod
    def from_dict(cls, cipherparams):
        new_cipherparams = cls.__new__(cls)
        for key in cipherparams:
            setattr(new_cipherparams, key, cipherparams[key])
        return new_cipherparams

    @property
    def iv(self):
        return self._iv

    @iv.setter
    def iv(self, iv):
        self._iv = iv
```

CryptoStruct

```python

class CryptoStruct:
    def __init__(
        self,
        cipher: int,
        ciphertext: str,
        cipherparams: CipherParams,
        kdf: str,
        kdfparams: KdfParams,
        mac: str,
    ):
        self._cipher = cipher
        self._ciphertext = ciphertext
        self._cipherparams = cipherparams
        self._kdf = kdf
        self._kdfparams = kdfparams
        self._mac = mac

    @classmethod
    def from_dict(cls, crypto):
        new_crypto = cls.__new__(cls)
        for key in crypto:
            setattr(new_crypto, key, crypto[key])
        return new_crypto

    @property
    def cipher(self):
        return self._cipher

    @cipher.setter
    def cipher(self, cipher):
        self._cipher = cipher

    @property
    def ciphertext(self):
        return self._ciphertext

    @ciphertext.setter
    def ciphertext(self, ciphertext):
        self._ciphertext = ciphertext

    @property
    def cipherparams(self):
        return self._cipherparams

    @cipherparams.setter
    def cipherparams(self, cipherparams):
        if isinstance(cipherparams, dict):
            self._cipherparams = CipherParams.from_dict(cipherparams)
        else:
            self._cipherparams = cipherparams

    @property
    def kdf(self):
        return self._kdf

    @kdf.setter
    def kdf(self, kdf):
        self._kdf = kdf

    @property
    def kdfparams(self):
        return self._kdfparams

    @kdfparams.setter
    def kdfparams(self, kdfparams):
        if isinstance(kdfparams, dict):
            self._kdfparams = KdfParams.from_dict(kdfparams)
        else:
            self._kdfparams = kdfparams

    @property
    def mac(self):
        return self._mac

    @mac.setter
    def mac(self, mac):
        self._mac = mac
```

KdfParams

```python

class KdfParams:
    def __init__(self, prf:str , dklen:int , salt:str , c:int):
        self._prf = prf
        self._dklen = dklen
        self._salt = salt
        self._c = c

    @classmethod
    def from_dict(cls, kdfparams):
        new_kdfparams = cls.__new__(cls)
        for key in kdfparams:
            setattr(new_kdfparams, key, kdfparams[key])
        return new_kdfparams
    
    @property
    def prf(self):
        return self._prf

    @prf.setter
    def prf(self, prf):
        self._prf = prf

    @property
    def dklen(self):
        return self._dklen
    
    @dklen.setter
    def dklen(self, dklen):
        self._dklen = dklen
    
    @property
    def salt(self):
        return self._salt

    @salt.setter
    def salt(self, salt):
        self._salt = salt

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, c):
        self._c = c
```
## Tests

These packages needed to run tests:

- pytest `pip install pytest`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_crypto/tests
```
