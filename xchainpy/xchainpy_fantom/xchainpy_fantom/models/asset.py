from xchainpy_util.asset import Asset as base
from xchainpy_util.chain import is_chain


class Asset(base):
    _contract = ''

    def __init__(self, chain, symbol, ticker='', contract=''):
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
                self._ticker = symbol[0:symbol.index('-')]
            else:
                self._ticker = symbol
        else:
            self._ticker = ticker
        if not contract:
            if ':' in symbol:
                self._contract = symbol[symbol.index(':')+1:]
            else:
                self._contract = symbol
        else:
            self._contract = contract

    def __str__(self):
        """Get an asset from a string

        :returns: the asset (BNB.BNB or BNB.RUNE)
        """
        return f'{self.chain}.{self.symbol}:{self.contract}'

    @property
    def contract(self):
        return self._contract

    @contract.setter
    def contract(self, contract):
        self._contract = contract
