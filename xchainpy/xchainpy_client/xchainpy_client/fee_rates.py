from . models.types import FeeRates

def standard_fee_rates(rate):
    return FeeRates(fast=rate, fastest=rate*5, average=rate*0.5)