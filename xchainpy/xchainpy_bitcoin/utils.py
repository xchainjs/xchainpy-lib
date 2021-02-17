from typing import List, Optional, Union
import asyncio
from xchainpy.xchainpy_bitcoin.const import MIN_TX_FEE
from xchainpy.xchainpy_bitcoin.models.common import DerivePath, UTXO
from bitcoinlib.services.services import *
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models.balance import Balance
from xchainpy.xchainpy_util.chain import BTCCHAIN
from xchainpy.xchainpy_client.models import tx_types
import datetime
import binascii


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


def calc_fee(fee_rate , memo=''):
    compiled_memo = compile_memo(memo) if memo else None
    fee = get_fee([] , fee_rate , compiled_memo)
    return fee

def compile_memo(memo : str):
    # data = memo.encode('utf-8').hex()
    data = bytes(memo , 'utf-8')
    # raw = binascii.a2b_hex(data)
    return data

def get_fee(inputs : List[UTXO] , fee_rate : float , data : Optional[bytes] = None):
    lst_reduce = functools.reduce(lambda a , x : a + input_bytes(x),inputs) if len(inputs) > 0 else 0 
    sum = TX_EMPTY_SIZE + lst_reduce + len(inputs) + TX_OUTPUT_BASE + TX_OUTPUT_PUBKEYHASH + TX_OUTPUT_BASE + TX_OUTPUT_PUBKEYHASH
    if data:
        sum = sum + TX_OUTPUT_BASE + len(data)
    fee = sum * fee_rate
    result = fee if fee > MIN_TX_FEE else MIN_TX_FEE
    return result

def input_bytes(input : UTXO):
    result = TX_INPUT_BASE + (len(input.witness_utxo['script']) if input.witness_utxo['script'] else TX_INPUT_PUBKEYHASH)
    return result
