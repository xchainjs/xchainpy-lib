from xchainpy.xchainpy_crypto.models.KdfParams import KdfParams
from xchainpy.xchainpy_crypto.models.CipherParams import CipherParams


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
        self.__cipher = cipher
        self.__ciphertext = ciphertext
        self.__cipherparams = cipherparams
        self.__kdf = kdf
        self.__kdfparams = kdfparams
        self.__mac = mac

    @property
    def cipher(self):
        return self.__cipher

    @cipher.setter
    def cipher(self, cipher):
        self.__cipher = cipher

    @property
    def ciphertext(self):
        return self.__ciphertext

    @ciphertext.setter
    def ciphertext(self, ciphertext):
        self.__ciphertext = ciphertext

    @property
    def cipherparams(self):
        return self.__cipherparams

    @cipherparams.setter
    def cipherparams(self, cipherparams):
        self.__cipherparams = cipherparams

    @property
    def kdf(self):
        return self.__kdf

    @kdf.setter
    def kdf(self, kdf):
        self.__kdf = kdf

    @property
    def kdfparams(self):
        return self.__kdfparams

    @kdfparams.setter
    def kdfparams(self, kdfparams):
        self.__kdfparams = kdfparams

    @property
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, mac):
        self.__mac = mac

    def __getitem__(self, item):
         return getattr(self, item)
