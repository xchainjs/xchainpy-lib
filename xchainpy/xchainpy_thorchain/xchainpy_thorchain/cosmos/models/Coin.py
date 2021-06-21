class Coin:
    def __init__(self, denom : str , amount : str):
        self._denom = denom
        self._amount = amount

    @property
    def denom(self):
        return self._denom

    @denom.setter
    def denom(self, denom):
        self._denom = denom

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount