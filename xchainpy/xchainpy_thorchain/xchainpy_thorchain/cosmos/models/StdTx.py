import json
from typing import List, Optional, Union
from xchainpy.xchainpy_thorchain.xchainpy_thorchain.utils import sort_dict
from .StdSignature import StdSignature
from .StdTxFee import StdTxFee
from .AminoWrapping import AminoWrapping
from .Msg import Msg
from .Tx import Tx


class StdTx(Tx):
    def __init__(self, msg : Union[Msg , AminoWrapping] , fee : StdTxFee , signatures : Optional[List[StdSignature]] , memo : str):
        self._msg = msg
        self._fee = fee
        self._signatures = signatures
        self._memo = memo

    @property
    def msg(self):
        return self._msg

    @msg.setter
    def msg(self, msg):
        self._msg = msg

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self, fee):
        self._fee = fee

    @property
    def signature(self):
        return self._signatures

    @signature.setter
    def signature(self, signature):
        self._signatures = signature

    @property
    def memo(self):
        return self._memo

    @memo.setter
    def memo(self, memo):
        self._memo = memo

    def get_sign_bytes(self , chain_id : str , account_number : str , sequence : str):
        std_sign_msg = {
            "account_number" : account_number,
            "chain_id" : chain_id,
            "fee" : self._fee,
            "memo" : self._memo,
            "msgs" : self._msg,
            "sequence" : sequence
        }

        canonicalized = sort_dict(std_sign_msg)
        json_object = json.dumps(canonicalized)
        encoded = json_object.encode('utf8')
        encoded_bytes = bytearray(encoded)
        
        return encoded_bytes
    
    def to_json(self):
        return json.dumps(self, default=lambda o: {key.lstrip('_'): value for key, value in o.__dict__.items()})