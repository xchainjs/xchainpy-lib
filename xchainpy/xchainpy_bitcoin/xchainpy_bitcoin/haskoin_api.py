import asyncio
import json
import http3
from . models.common import UTXO, Witness_UTXO
from . sochain_api import get_is_tx_confirmed
from xchainpy_client.models.balance import Balance
from xchainpy_util.asset import AssetBTC

HASKOIN_API_URL = 'https://api.haskoin.com/btc'

def haskoin_utxo_to_xchain_utxo(utxo):
    """Get utxo object from a sochain utxo

    :param utxo: haskoin utxo
    :type utxo: dict
    :returns: UTXO object
    """
    hash = utxo['txid']
    index = utxo['index']
    value = int(float(utxo['value']) * 10 ** 8)
    script =  bytearray.fromhex(utxo['pkscript']) #utxo['script_hex']
    witness_utxo = Witness_UTXO(value, script)
    return UTXO(hash, index, witness_utxo)

async def get_balance(address:str):
    """Get address balance
    https://api.haskoin.com/#/Address/getBalance

    :param address: wallet address
    :type address: str
    :returns: BTC balance
    """
    try:
        api_url = f'{HASKOIN_API_URL}/address/{address}/balance'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            balance_response = json.loads(response.content.decode('utf-8'))
            confirmed = float(balance_response['confirmed'])
            unconfirmed = float(balance_response['unconfirmed'])
            total = confirmed + unconfirmed
            balance = [Balance(asset=AssetBTC, amount=total)]
            return balance
        else:
            return None
    except Exception as err:
        raise Exception(str(err))

async def get_unspent_txs(address):
    """Get address balance
    https://api.haskoin.com/#/Address/getAddressUnspent

    :param address: address
    :type address: str
    :returns: A list of utxo's
    """
    try:
        api_url = f'{HASKOIN_API_URL}/address/{address}/unspent'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            txs = json.loads(response.content.decode('utf-8'))
            return txs

    except Exception as err:
        raise Exception(str(err))

async def get_confirmed_unspent_txs(address):
    """Get address balance
    https://api.haskoin.com/#/Address/getAddressUnspent

    :param address: address
    :type address: str
    :returns: A list confirmed of utxo's
    """
    txs = await get_unspent_txs(address)
    confirmed_UTXOs = await asyncio.wait([get_is_tx_confirmed(tx, True) for tx in txs])

    return confirmed_UTXOs