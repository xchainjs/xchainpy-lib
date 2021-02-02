from xchainpy.xchainpy_crypto.models.CryptoStruct import CryptoStruct


class Keystore:
    def __init__(self, crypto: CryptoStruct, id: str, version: int, meta: str):
        self.__crypto = crypto
        self.__id = id
        self.__version = version
        self.__meta = meta

    @property
    def crypto(self):
        return self.__crypto

    @crypto.setter
    def crypto(self, crypto):
        self.__crypto = crypto

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version

    @property
    def meta(self):
        return self.__meta

    @meta.setter
    def meta(self, meta):
        self.__meta = meta
