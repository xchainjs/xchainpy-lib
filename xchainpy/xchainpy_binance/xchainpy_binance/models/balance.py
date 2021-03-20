from xhchainpy-util import Asset
from xchainpy-client.models.balance import Balance
from xchainpy-util.chain import BNBCHAIN

class BinanceBalance(Balance):

    def __init__(self, balance):
        """
        :param balance: binance balance object
        :type balance: a dict contains: free, frozen, locked, symbol
        """
        asset = Asset(BNBCHAIN, balance['symbol'])
        super().__init__(asset, balance['free'])