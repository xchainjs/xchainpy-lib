from .models.MsgCoin import MsgCoin
from .models.MsgNativeTx import MsgNativeTx

def msg_native_tx_from_json(coins : list[MsgCoin] , memo : str , signer : str) -> MsgNativeTx :
    return MsgNativeTx(coins , memo , signer)
