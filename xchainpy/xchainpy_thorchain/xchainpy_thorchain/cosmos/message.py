from sys import prefix
from typing import List
from .models.MsgCoin import MsgCoin
from .models.MsgNativeTx import MsgNativeTx
import bech32
from ..utils import bech32_fromwords, frombech32

def msg_native_tx_from_json(coins : List[MsgCoin] , memo : str , signer : str) -> MsgNativeTx :
    return MsgNativeTx(coins , memo , frombech32(signer))

