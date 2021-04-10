class MsgCoin:
    def __init__(self, asset : str , amount : str):
        self._asset = asset
        self._amount = amount

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset):
        self._asset = asset

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount