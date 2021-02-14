from typing import Union
import asyncio
from xchainpy.xchainpy_bitcoin.models.common import DerivePath
from bitcoinlib.services.services import *
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models.balance import Balance
from xchainpy.xchainpy_util.chain import BTCCHAIN
from xchainpy.xchainpy_client.models import tx_types
import datetime


TX_EMPTY_SIZE = 4 + 1 + 1 + 4 #10
TX_INPUT_BASE = 32 + 4 + 1 + 4 #41
TX_INPUT_PUBKEYHASH = 107
TX_OUTPUT_BASE = 8 + 1 #9
TX_OUTPUT_PUBKEYHASH = 25
DUST_THRESHOLD = 1000


def get_derive_path(index:int=0):
    return DerivePath(index=index)

def parse_tx(tx):
    """Parse tx

    :param tx: The transaction to be parsed
    :type tx: str
    :returns: The transaction parsed from the binance tx
    """
    asset = Asset.from_str(f'{BTCCHAIN}.BTC')
    tx_from = [tx_types.TxFrom(i['address'], i['value']) for i in tx['inputs']]
    tx_to = [tx_types.TxTo(i['address'], i['value']) for i in tx['outputs']]
    tx_date = datetime.datetime.fromtimestamp(tx['time'])
    tx_type = 'transfer'
    tx_hash = tx['txid']

    tx = tx_types.TX(asset, tx_from, tx_to, tx_date, tx_type, tx_hash)
    return tx