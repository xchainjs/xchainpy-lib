from xchainpy_util import chain

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
        if chain.is_chain(chain):
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
    
    def asset_to_string(self):
        """Get an asset from a string

        :returns: the asset (BNB.BNB or BNB.RUNE)
        """
        return f'{self.chain}.{self.symbol}'