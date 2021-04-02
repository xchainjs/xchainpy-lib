from  .chain import is_chain

class Asset:
    _chain = None # "BNB" | "BTC" | "ETH" | "THOR" | "GAIA" | "POLKA"
    _symbol = _ticker = '' 

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
            self._chain = chain
        else:
            raise Exception('the chain is invalid')
        self._symbol = symbol
        if not ticker:
            if '-' in symbol:
                self._ticker = symbol[0:symbol.index('-')]
            else:
                self._ticker = symbol
        else:
            self._ticker = ticker

    @classmethod
    def from_str(cls, asset_str):
        chain = asset_str[0:asset_str.index('.')]
        symbol = asset_str[asset_str.index('.')+1:]
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

    @property
    def chain(self):
        return self._chain

    @chain.setter
    def chain(self, chain):
        self._chain = chain

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        self._symbol = symbol

    @property
    def ticker(self):
        return self._ticker

    @ticker.setter
    def ticker(self, ticker):
        self._ticker = ticker