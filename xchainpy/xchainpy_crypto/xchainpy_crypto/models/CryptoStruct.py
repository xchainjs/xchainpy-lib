from .KdfParams import KdfParams
from .CipherParams import CipherParams


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