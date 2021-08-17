from abc import ABC, abstractmethod
import logging

from . base_xchain_client import BaseXChainClient 
from . fee_rates import standard_fee_rates
from . models.types import FeesWithRates
from . fees import calc_fees

class UTXOClient(BaseXChainClient):

    @abstractmethod
    async def _get_suggested_fee_rate(self):
        pass
    
    @abstractmethod
    def calc_fee(self, fee_rate, memo:str=None):
        pass

    async def get_fees_with_rates(self, memo:str=None):
        """Get the rates and fees

        :param memo: The memo to be used for fee calculation (optional)
        :type memo: str
        :returns: A FeesWithRates object
        """
        rates = await self.get_fee_rates()
        fees = calc_fees(rates, self._calc_fee, memo)
        return FeesWithRates(fees=fees,rates=rates)

    async def get_fees(self, memo:str=None):
        """Get the fees for transactions with or without memo
        If you want to get `fees` and `fee_rates` at once, use `get_fees_with_rates` method

        :param memo: The memo to be used for fee calculation (optional)
        :type memo: str
        :returns: The fees
        """
        try:
            fees = (await self.get_fees_with_rates(memo)).fees
            return fees
        except Exception as err:
            raise Exception(str(err))

    async def get_fee_rates(self):
        """Get the fee rates for transactions without a memo
        If you want to get `fees` and `fee_rates` at once, use `get_fees_with_rates` method

        :returns: The fee rate
        """
        try:
            fee_rate = await self.get_fee_rate_from_thorchain()
        except Exception as err:
            logging.warning(str(err))

            fee_rate = await self._get_suggested_fee_rate()

        return standard_fee_rates(fee_rate)