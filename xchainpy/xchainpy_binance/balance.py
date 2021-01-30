from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_util.balance import Balance
from xchainpy.xchainpy_util.chain import BNBCHAIN

class BinanceBalance(Balance):
    asset = None # Asset
    amount = 0

    def __init__(self, balance):
        """
        :param balance: binance balance object
        :type balance: a dict contains: free, frozen, locked, symbol
        """
        asset = Asset(BNBCHAIN, balance['symbol'])
        super().__init__(asset, balance['free'])