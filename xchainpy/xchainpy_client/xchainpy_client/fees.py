from . models.types import Fees

def standard_fees(fee):
    return Fees(fast=fee, fastest=fee*5, average=fee*0.5)

def calc_fees(rates, calc_fee, memo):
    fast = calc_fee(rates.fast, memo)
    fastest = calc_fee(rates.fastest, memo)
    average = calc_fee(rates.average, memo)
    return Fees(fast=fast, fastest=fastest, average=average)