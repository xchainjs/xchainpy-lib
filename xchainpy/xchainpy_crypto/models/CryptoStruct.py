from xchainpy.xchainpy_crypto.models.KdfParams import KdfParams
from xchainpy.xchainpy_crypto.models.CipherParams import CipherParams


class CryptoStruct:
    def __init__(
        self,
        cipher: int,
        cipher_text: str,
        cipher_params: CipherParams,
        kdf: str,
        kdf_params: KdfParams,
        mac: str,
    ):
        self.__cipher = cipher
        self.__cipher_text = cipher_text
        self.__cipher_params = cipher_params
        self.__kdf = kdf
        self.__kdf_params = kdf_params
        self.__mac = mac

    @property
    def cipher(self):
        return self.__cipher

    @cipher.setter
    def cipher(self, cipher):
        self.__cipher = cipher

    @property
    def cipher_text(self):
        return self.__cipher_text

    @cipher_text.setter
    def cipher_text(self, cipher_text):
        self.__cipher_text = cipher_text

    @property
    def cipher_params(self):
        return self.__cipher_params

    @cipher_params.setter
    def cipher_params(self, cipher_params):
        self.__cipher_params = cipher_params

    @property
    def kdf(self):
        return self.__kdf

    @kdf.setter
    def kdf(self, kdf):
        self.__kdf = kdf

    @property
    def kdf_params(self):
        return self.__kdf_params

    @kdf_params.setter
    def kdf_params(self, kdf_params):
        self.__kdf_params = kdf_params

    @property
    def mac(self):
        return self.__mac

    @mac.setter
    def mac(self, mac):
        self.__mac = mac
