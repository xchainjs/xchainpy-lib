from xchainpy.xchainpy_util.chain import is_chain

class Asset:
    chain = None # "BNB" | "BTC" | "ETH" | "THOR" | "GAIA" | "POLKA"
    symbol = ticker = '' 

    def __init__(self, chain, symbol, ticker = ''):
        """
        :param chian: chain type
        :type chain: str
        :param symbol: symbol name
        :type symbol: str
        :param ticker: is the symbol or a part of that
        :type ticker: str
        """
        if is_chain(chain):
            self.chain = chain
        else:
            raise Exception('the chain is invalid')
        self.symbol = symbol
        if not ticker:
            if '-' in symbol:
                self.ticker = symbol[0:symbol.index('-')]
            else:
                self.ticker = symbol
        else:
            self.ticker = ticker

    @classmethod
    def from_str(cls, asset_str):
        chain = asset_str[0:asset_str.index('.')]
        symbol = asset_str[asset_str.index('.'):]
        return Asset(chain, symbol)


    def __str__(self):
        """Get an asset from a string

        :returns: the asset (BNB.BNB or BNB.RUNE)
        """
        return f'{self.chain}.{self.symbol}'


    def __eq__(self, asset):
        """get are two assets equal or not

        :param asset: an asset
        :type asset: Asset
        :returns: the assets are equal or not
        """
        return str(self) == str(asset)

    def __getitem__(self, item):
         return getattr(self, item)