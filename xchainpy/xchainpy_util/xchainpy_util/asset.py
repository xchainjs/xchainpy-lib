from . chain import Chain, is_chain

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

"""
Base "chain" asset of Binance chain.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetBNB = Asset(chain=Chain.Binance, symbol='BNB', ticker='BNB')

"""
Base "chain" asset on bitcoin main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetBTC = Asset(chain=Chain.Bitcoin, symbol='BTC', ticker='BTC')

"""
Base "chain" asset on bitcoin cash main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetBCH = Asset(chain=Chain.BitcoinCash, symbol='BCH', ticker='BCH')

"""
Base "chain" asset on litecoin main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetLTC = Asset(chain=Chain.Litecoin, symbol='LTC', ticker='LTC')

"""
Base "chain" asset on ethereum main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetETH = Asset(chain=Chain.Ethereum, symbol='ETH', ticker='ETH')

RUNE_TICKER = 'RUNE'

"""
Base "chain" asset for RUNE-67C on Binance test net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetRune67C = Asset(chain=Chain.Binance, symbol='RUNE-67C', ticker=RUNE_TICKER)

"""
Base "chain" asset for RUNE-B1A on Binance main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetRuneB1A = Asset(chain=Chain.Binance, symbol='RUNE-B1A', ticker=RUNE_TICKER)

"""
Base "chain" asset on thorchain main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetRuneNative = Asset(chain=Chain.THORChain, symbol=RUNE_TICKER, ticker=RUNE_TICKER)

"""
Base "chain" asset for RUNE on ethereum main net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetRuneERC20 = Asset(chain=Chain.Ethereum, symbol=f'{RUNE_TICKER}-0x3155ba85d5f96b2d030a4966af206230e46849cb', ticker=RUNE_TICKER)

"""
Base "chain" asset for RUNE on ethereum test net.
Based on definition in Thorchain `common`
@see https://gitlab.com/thorchain/thornode/-/blob/master/common/asset.go#L12-24
"""
AssetRuneERC20 = Asset(chain=Chain.Ethereum, symbol=f'{RUNE_TICKER}-0xd601c6A3a36721320573885A8d8420746dA3d7A0', ticker=RUNE_TICKER)