class KdfParams:
    def __init__(self, prf : str , dklen : int , salt : str , c : int):
      self.__prf = prf
      self.__dklen = dklen
      self.__salt = salt
      self.__c = c
    
    @property
    def prf(self):
        return self.__prf

    @prf.setter
    def prf(self, prf):
        self.__prf = prf

    @property
    def dklen(self):
        return self.__dklen
    
    @dklen.setter
    def dklen(self, dklen):
        self.__dklen = dklen
    
    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, salt):
        self.__salt = salt

    @property
    def c(self):
        return self.__c

    @c.setter
    def c(self, c):
        self.__c = c