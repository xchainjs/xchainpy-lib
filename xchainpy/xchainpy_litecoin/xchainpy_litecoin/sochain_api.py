import json
import http3
from xchainpy_client.models.balance import Balance
from xchainpy_util.asset import AssetLTC

DEFAULT_SUGGESTED_TRANSACTION_FEE = 1

def to_sochain_network(network: str):
    return 'LTCTEST' if network == 'testnet' else 'LTC'

async def get_balance(sochain_url:str, network:str, address:str):
    """Get address balance
    https://sochain.com/api#get-balance

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: mainnet or testnet
    :type network: str
    :param address: wallet address
    :type address: str
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
            balance = [Balance(asset=AssetLTC, amount=total)]
            return balance
        else:
            return None
    except Exception as err:
        raise Exception(str(err))


async def get_transactions(sochain_url:str, network:str, address:str):
    """Get address information
    https://sochain.com/api#get-display-data-address

    :param sochain_url: sochain url
    :type sochain_url: str
    :param network: mainnet or testnet
    :type network: str
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
    """Get Litecoin suggested transaction fee

    Note: sochain does not provide fee rate related data
    So use Bitgo API for fee estimation
    Refer: https://app.bitgo.com/docs/#operation/v2.tx.getfeeestimate

    :returns: The Litecoin suggested transaction fee per bytes in sat
    """
    try:
        api_url = 'https://app.bitgo.com/api/v2/ltc/tx/fee'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))['feePerKb'] / 1000 # feePerKb to feePerByte
        else:
            return DEFAULT_SUGGESTED_TRANSACTION_FEE
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
                txs = txs + next_batch
            return txs
    except Exception as err:
        raise Exception(str(err))

async def broadcast_tx(sochain_url, network, tx_hex):
    """Broadcast transaction
    https://sochain.com/api#send-transaction

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