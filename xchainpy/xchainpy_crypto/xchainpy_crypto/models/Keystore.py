from .CryptoStruct import CryptoStruct
import json


class Keystore:
    def __init__(self, crypto: CryptoStruct, id:str, version:int, meta:str):
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
