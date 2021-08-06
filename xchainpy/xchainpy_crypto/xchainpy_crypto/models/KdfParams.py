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