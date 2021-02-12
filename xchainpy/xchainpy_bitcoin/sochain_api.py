import json
import http3

api_url_base = 'https://sochain.com/api/v2/'


def to_sochain_network(net: str):
    return 'BTCTEST' if net == 'testnet' else 'BTC'


async def get_transactions(net: str, address: str):
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


async def get_suggested_tx_fee(net: str, hash: str):
    # Note: sochain does not provide fee rate related data
    # This number is from https://bitcoinfees.earn.com API
    # Refer: https://bitcoinfees.earn.com/api
    try:
        api_url = 'https://bitcoinfees.earn.com/api/v1/fees/recommended'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['data']['fastestFee']
        else:
            return None
    except Exception as err:
        raise Exception(str(err))
