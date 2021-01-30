from xchainpy.xchainpy_util.asset import Asset

class Balance:
    asset = None # Asset
    amount = 0

    def __init__(self, asset, amount):
        """
        :param asset: asset type
        :type asset: Asset
        :param amount: amount 
        :type amount: str
        """
        self.asset = asset
        self.amount = amount

    def __getitem__(self, item):
         return getattr(self, item)