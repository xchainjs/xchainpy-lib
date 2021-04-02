class MultiTransfer:
    def __init__(self, coins, recipient: str):
        if type(coins, list):
            self._coins = coins
        else:
            raise Exception('coins should be a list of Coin objects')

        self._recipient = recipient

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, coins):
        self._coins = coins

    @property
    def recipient(self):
        return self._recipient

    @recipient.setter
    def recipient(self, recipient):
        self._recipient = recipient