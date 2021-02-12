from typing import Union
from xchainpy.xchainpy_bitcoin.models.common import DerivePath

TX_EMPTY_SIZE = 4 + 1 + 1 + 4 #10
TX_INPUT_BASE = 32 + 4 + 1 + 4 #41
TX_INPUT_PUBKEYHASH = 107
TX_OUTPUT_BASE = 8 + 1 #9
TX_OUTPUT_PUBKEYHASH = 25
DUST_THRESHOLD = 1000


def get_derive_path(index:int=0):
    return DerivePath(index=index)
