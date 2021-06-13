from .Msg import Msg
import json

class MsgCoin(Msg):
    def __init__(self, asset : str , amount : str):
        self._asset = asset
        self._amount = amount

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset):
        self._asset = asset

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount
    
    def to_json(self):
        return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()})

    def to_obj(self):
        data = {key.lstrip('_'): str(value) for key, value in self.__dict__.items()}
        return data