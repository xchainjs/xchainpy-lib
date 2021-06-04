from xchainpy_util.asset import Asset as template
from xchainpy_util.chain import is_chain


class Asset(template):
    def __init__(self, chain, symbol, ticker = ''):
        """
        :param chain: chain type
        :type chain: str
        :param symbol: symbol name
        :type symbol: str
        :param ticker: is the symbol or the contract address of the token
        :type ticker: str
        """

        if is_chain(chain):
            self._chain = chain
        else:
            raise Exception('the chain is invalid')
        self._symbol = symbol
        if not ticker:
            if '-' in symbol:
                self._ticker = symbol[symbol.index('-')+1:]
            else:
                self._ticker = symbol
        else:
            self._ticker = ticker