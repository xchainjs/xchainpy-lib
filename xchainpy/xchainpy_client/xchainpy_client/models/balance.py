from xchainpy_util.asset import Asset


class Balance:
    _asset = None  # Asset
    _amount = 0

    def __init__(self, asset, amount):
        """
        :param asset: asset type
        :type asset: Asset
        :param amount: amount 
        :type amount: str
        """
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
