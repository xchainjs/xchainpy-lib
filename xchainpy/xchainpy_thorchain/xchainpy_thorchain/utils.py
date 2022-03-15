from .cosmos.cosmosUtil import bech32_prefix 
import bech32
import http3
import json

DECIMAL = 8
DEFAULT_GAS_VALUE = 3000000
DEPOSIT_GAS_VALUE = 500000000
MAX_TX_COUNT = 100

DEFAULT_EXPLORER_URL = "https://viewblock.io/thorchain"


def get_default_explorer_urls():
    """Get the explorer url.

    :returns: The explorer url (both mainnet and testnet) for thorchain.
    :rtype: string
    """
    root = {
        "testnet": f'{DEFAULT_EXPLORER_URL}?network=testnet',
        "stagenet": f'{DEFAULT_EXPLORER_URL}?network=stagenet',
        "mainnet" : DEFAULT_EXPLORER_URL,
    }

    txUrl = f'{DEFAULT_EXPLORER_URL}/tx'
    tx = {
        "testnet": txUrl,
        "stagenet": txUrl,
        "mainnet" : txUrl,
    }
    addressUrl = f'{DEFAULT_EXPLORER_URL}/address'
    address = {
        "testnet": addressUrl,
        "stagenet": addressUrl,
        "mainnet" : addressUrl,
    }
    
    return {
        root,
        tx,
        address
    }

def base_amount(value: str and int, decimal: int = DECIMAL) -> str:
    if type(value) == int:
        return str(value / 10**decimal)
    else:
        return str(int(value) / 10**decimal)


def cnv_big_number(value: float and int and str, decimal: int = DECIMAL) -> str:
    if type(value) == float or type(value) == int:
        return str(round(float(value) * (10**decimal)))
    elif type(value) == str:
        return str(round(float(value) * (10**decimal)))


def getDenomWithChain(asset) -> str:
    return f'THOR.{asset["symbol"].upper()}'


def bech32_fromwords(words):
    res = bech32.convertbits(words, 5, 8, False)
    if res:
        return res


def bech32_towords(value_bytes):
    res = bech32.convertbits(value_bytes, 8, 5, False)
    if res:
        return res
    

def frombech32(address : str):
    (prefix, words) = bech32.bech32_decode(address)
    res = bech32_fromwords(words)
    return res


def tobech32(value):
    words = bech32_towords(bytes(value))
    enc = bech32.bech32_encode(bech32_prefix["accAddr"], words)
    return enc


def sort_dict(item: dict):
    return {k: sort_dict(v) if isinstance(v, dict) else v for k, v in sorted(item.items())}    


def get_asset(denom : str):
    if denom == 'rune':
        return  {"chain" : "THOR", "symbol": "RUNE" , "ticker" : "RUNE"}
    else:
        
        return  {"chain" : "THOR", "symbol": denom.upper() , "ticker" : denom.split('-')[0]}


def asset_to_string(asset):
    return f'{asset["chain"]}.{asset["symbol"]}'

async def get_chain_id(node_url : str) -> str:
    try:
        url = f'{node_url}/cosmos/base/tendermint/v1beta1/node_info'
        client = http3.AsyncClient(timeout=10)
        response = await client.get(url)
        if  response.status_code == 200:
            res = json.loads(response.content.decode('utf-8'))['data']
            if res:
                if res['default_node_info']:
                    if res['default_node_info']['network']:
                        return res['default_node_info']['network']
            else:
                raise Exception("Could not parse chain id")  
    except Exception as err:
        raise Exception(err)