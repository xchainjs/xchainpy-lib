class StdSignature:
    def __init__(self, pub_key , signature : str):
        self._pub_key = pub_key
        self._signature = signature

    @property
    def pub_key(self):
        return self._pub_key

    @pub_key.setter
    def pub_key(self, pub_key):
        self._pub_key = pub_key

    @property
    def signature(self):
        return self._signature

    @signature.setter
    def signature(self, signature):
        self._signature = signature