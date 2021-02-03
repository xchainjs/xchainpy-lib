class CipherParams:
    def __init__(self, iv: str):
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