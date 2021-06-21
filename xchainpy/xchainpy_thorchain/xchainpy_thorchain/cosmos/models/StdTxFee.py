from typing import List
from .Coin import Coin
import json


class StdTxFee:
    def __init__(self, gas : str , amount : List[Coin]):
        self._gas = gas
        self._amount = amount

    @property
    def gas(self):
        return self._gas

    @gas.setter
    def asset(self, gas):
        self._gas = gas

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    def to_json(self):
        return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()})