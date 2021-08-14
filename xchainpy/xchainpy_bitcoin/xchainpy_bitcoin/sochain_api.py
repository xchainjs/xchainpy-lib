import json
from . models.common import UTXO, Witness_UTXO
import http3
import asyncio
from xchainpy_client.models.balance import Balance
from xchainpy_util.asset import AssetBTC

DEFAULT_SUGGESTED_TRANSACTION_FEE = 127

def to_sochain_network(net: str):
    return 'BTCTEST' if net == 'testnet' else 'BTC'

def sochain_utxo_to_xchain_utxo(utxo):
    """Get utxo object from a sochain utxo

    :param utxo: sochain utxo
    :type utxo: dict
    :returns: UTXO object
    """
    hash = utxo['txid']
    index = utxo['output_no']
    value = int(float(utxo['value']) * 10 ** 8)
    script =  bytearray.fromhex(utxo['script_hex']) #utxo['script_hex']
    witness_utxo = Witness_UTXO(value, script)
    return UTXO(hash, index, witness_utxo)


async def get_transactions(sochain_url:str, network:str, address:str):
    """Get address information
    https://sochain.com/api#get-display-data-address

    :param sochain_url: sochain url
    :type sochain_url: str
    :param net: mainnet or testnet
    :type net: str
    :param address: wallet address
    :type address: str
    :returns: The fees with memo
    """
    try:
        api_url = f'{sochain_url}/address/{to_sochain_network(network)}/{address}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['data']
        else:
            return None
    except Exception as err:
        raise Exception(str(err))


async def get_tx(sochain_url:str, network:str, hash:str):
    """Get transaction by hash
    https://sochain.com/api#get-tx

    :param sochain_url: sochain url
    :type sochain_url: str
    :param net: mainnet or testnet
    :type net: str
    :param hash: The transaction hash
    :type hash: str
    :returns: The fees with memo
    """
    try:
        api_url = f'{sochain_url}/get_tx/{to_sochain_network(network)}/{hash}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['data']
        else:
            return None
    except Exception as err:
        raise Exception(str(err))


async def get_suggested_tx_fee():
    """Get Bitcoin suggested transaction fee
    Note: sochain does not provide fee rate related data
    Refer: https://app.bitgo.com/api/v2/btc/tx/fee

    :returns: The Bitcoin suggested transaction fee per bytes in sat
    """
    try:
        api_url = 'https://app.bitgo.com/api/v2/btc/tx/fee'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            response = json.loads(response.content.decode('utf-8'))
            return response['feePerKb'] / 1000
        else:
            return DEFAULT_SUGGESTED_TRANSACTION_FEE ###
    except Exception as err:
        raise Exception(str(err))


async def get_balance(sochain_url:str, network:str, address:str):
    """Get address balance
    https://sochain.com/api#get-balance

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: mainnet or testnet
    :type network: str
    :param address: wallet address
    :type address: str
    :param confirmed_only: only confirmed
    :type confirmed_only: str
    :returns: BTC balance
    """
    try:
        api_url = f'{sochain_url}/get_address_balance/{to_sochain_network(network)}/{address}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            balance_response = json.loads(response.content.decode('utf-8'))['data']
            confirmed = float(balance_response['confirmed_balance'])
            unconfirmed = float(balance_response['unconfirmed_balance'])
            total = confirmed + unconfirmed
            balance = [Balance(asset=AssetBTC, amount=total)]
            return balance
        else:
            return None
    except Exception as err:
        raise Exception(str(err))

async def get_unspent_txs(sochain_url, network, address, starting_from_tx_id=None):
    """Get Unspent transactions
    https://sochain.com/api#get-unspent-tx

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :param starting_from_tx_id: starting_from_tx_id
    :type starting_from_tx_id: str
    :returns: A list of utxo's
    """
    try:
        api_url = f'{sochain_url}/get_tx_unspent/{to_sochain_network(network)}/{address}'

        if starting_from_tx_id:
            api_url += f'/{starting_from_tx_id}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            txs = json.loads(response.content.decode('utf-8'))['data']['txs']
            if len(txs) == 100:
                # fetch the next batch
                last_tx_id = txs[99]['txid']
                next_batch = await get_unspent_txs(sochain_url, network, address, last_tx_id)
                txs = txs.extend(next_batch)
            return txs
    except Exception as err:
        raise Exception(str(err))

async def get_confirmed_unspent_txs(sochain_url, network, address):
    """Get confirmed Unspent transactions
    https://sochain.com/api#get-unspent-tx

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: A list confirmed of utxo's
    """
    txs = await get_unspent_txs(sochain_url, network, address)
    confirmed_UTXOs = await asyncio.gather(*[get_is_tx_confirmed(sochain_url, network, tx, True) for tx in txs])

    return confirmed_UTXOs

async def get_is_tx_confirmed(sochain_url, network, tx, return_if_is_confirmed):
    """Get is tx confirmed
    https://sochain.com/api/#get-is-tx-confirmed

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: mainnet or testnet
    :type network: str
    :param tx: transaction object
    :type tx: transaction object
    :returns: Confirmation object
    """
    try:
        api_url = f'{sochain_url}/is_tx_confirmed/{to_sochain_network(network)}/{tx["txid"]}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            response = json.loads(response.content.decode('utf-8'))['data']
            if return_if_is_confirmed:
                if response['is_confirmed']:
                    return tx
            return tx
        else:
            raise Exception(str(response.content.decode('utf-8')))
    except Exception as err:
        raise Exception(str(err))

async def broadcast_tx(sochain_url, network, tx_hex):
    """Broadcast transaction
    https://sochain.com/api#send-transaction

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: testnet or mainnet
    :type network: str
    :param tx_hex: tranaction hex
    :type tx_hex: str
    :returns: Transaction ID
    """
    try:
        api_url = f'{sochain_url}/send_tx/{to_sochain_network(network)}'

        client = http3.AsyncClient(timeout=5)
        response = await client.post(url=api_url, data={'tx_hex': tx_hex})

        if response.status_code == 200:
            res = json.loads(response.content.decode('utf-8'))['data']
            return res['txid']
        else:
            return json.loads(response.content.decode('utf-8'))['data']
    except Exception as err:
        raise Exception(str(err))