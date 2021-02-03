class CipherParams:
    def __init__(self, iv: str):
        self.__iv = iv

    @property
    def iv(self):
        return self.__iv

    @iv.setter
    def iv(self, iv):
        self.__iv = iv

    def __getitem__(self, item):
         return getattr(self, item)