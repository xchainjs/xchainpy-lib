import json
import http3

api_url_base = 'https://sochain.com/api/v2/'


def to_sochain_network(net: str):
    return 'BTCTEST' if net == 'testnet' else 'BTC'


async def get_transactions(net: str, address: str):
    """Get address information
    https://sochain.com/api#get-display-data-address

    :param net: mainnet or testnet
    :type net: str
    :param address: wallet address
    :type address: str
    :returns: The fees with memo
    """
    try:
        api_url = f'{api_url_base}/address/{to_sochain_network(net)}/{address}'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['data']
        else:
            return None
    except Exception as err:
        raise Exception(str(err))


async def get_tx(net: str, hash: str):
    """Get transaction by hash
    https://sochain.com/api#get-tx

    :param net: mainnet or testnet
    :type net: str
    :param hash: The transaction hash
    :type hash: str
    :returns: The fees with memo
    """
    try:
        api_url = f'{api_url_base}/get_tx/{to_sochain_network(net)}/{hash}'

        client = http3.AsyncClient()
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
    This number is from https://bitcoinfees.earn.com API
    Refer: https://bitcoinfees.earn.com/api

    :returns: The Bitcoin suggested transaction fee per bytes in sat
    """
    try:
        api_url = 'https://bitcoinfees.earn.com/api/v1/fees/recommended'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['fastestFee']
        else:
            return None
    except Exception as err:
        raise Exception(str(err))


async def get_balance(net: str, address: str):
    """Get address balance
    https://sochain.com/api#get-balance

    :param net: mainnet or testnet
    :type net: str
    :param address: wallet address
    :type address: str
    :returns: The fees with memo
    """
    try:
        api_url = f'{api_url_base}/get_address_balance/{to_sochain_network(net)}/{address}'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            balance_response = json.loads(response.content.decode('utf-8'))['data']
            confirmed = float(balance_response['confirmed_balance'])
            unconfirmed = float(balance_response['unconfirmed_balance'])
            total = confirmed + unconfirmed
            return total
        else:
            return None
    except Exception as err:
        raise Exception(str(err))


async def get_unspent_txs(network, address):
    api_url = f'{api_url_base}/get_tx_unspent/{to_sochain_network(network)}/{address}'

    client = http3.AsyncClient()
    response = await client.get(api_url)

    if response.status_code == 200:
        txs = json.loads(response.content.decode('utf-8'))['data']['txs']
        return txs