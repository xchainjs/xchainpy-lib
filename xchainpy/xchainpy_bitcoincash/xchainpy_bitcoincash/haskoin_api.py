from typing import List
from . import utils
from .models.api_types import AddressBalance, Block, Transaction, TransactionInput, TransactionOutput, TxUnspent
import http3
import json

def to_haskoin_network(network: str):
    return 'bchtest' if network == 'testnet' else 'bch'

async def get_account(haskoin_url:str, network:str, address:str) -> AddressBalance:
    """Get account from address
    https://api.haskoin.com/#/Address/getBalance

    :param client_url: The haskoin API url
    :type client_url: str
    :param network: network
    :type network: str
    :param address: The BCH address
    :type address: str
    :returns: AddressBalance
    """
    try:
        api_url = f'{haskoin_url}/{to_haskoin_network(network)}/address/{address}/balance'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            balance_response = json.loads(response.content.decode('utf-8'))
            if "error" in balance_response:
                raise Exception(
                    f'Error is : {balance_response["error"]}\nMessage is : {balance_response["message"]}')
            else:
                result = AddressBalance(balance_response['received'], balance_response['utxo'], balance_response['address'],
                                        balance_response['txs'], balance_response['unconfirmed'], balance_response['confirmed'])
                return result
        else:
            return None
    except Exception as err:
        raise Exception(str(err))

async def get_transactions(haskoin_url:str, network:str, address:str, offset:int, limit:int):
    """Get address information
    https://api.haskoin.com/#/Address/getAddressTxsFull

    :param haskoin_url: haskoin url
    :type haskoin_url: str
    :param network: mainnet or testnet
    :type network: str
    :param address: wallet address
    :type address: str
    :returns: The fees with memo
    """
    try:
        api_url = f'{haskoin_url}/{to_haskoin_network(network)}/address/{address}/transactions/full'
        api_url += f'?offset={offset}&limit={limit}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            raise Exception('failed to query transactions')
    except Exception as err:
        raise Exception(str(err))


async def get_transaction(haskoin_url:str, network:str, tx_id:str):
    """Get transaction by hash
    https://api.haskoin.com/#/Transaction/getTransaction

    :param client_url: The haskoin API url
    :type client_url: str
    :param network: network
    :type network: str
    :param tx_id: The transaction id
    :type tx_id: str
    :returns: Transaction info
    :raises: 'failed to query transaction by a given hash' if failed to query transaction by a given hash
    """
    try:
        api_url = f'{haskoin_url}/{to_haskoin_network(network)}/transaction/{tx_id}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            result = json.loads(response.content.decode('utf-8'))
            return result
        else:
            raise Exception('failed to query transaction by a given hash')
    except Exception as err:
        raise Exception(str(err))


async def get_suggested_tx_fee():
    """Get suggested fee amount for Bitcoin cash. (fee per byte)

    Note: Haskcoin does not provide fee rate related data
    So use Bitgo API for fee estimation
    Refer: https://app.bitgo.com/docs/#operation/v2.tx.getfeeestimate

    :returns: The Bitcoin cash stats
    """
    try:
        api_url = 'https://app.bitgo.com/api/v2/bch/tx/fee'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            fee_response = json.loads(response.content.decode('utf-8'))
            return fee_response["feePerKb"] / 1000 # feePerKb to feePerByte
        else:
            fee_response = json.loads(response.content.decode('utf-8'))
            if "error" in fee_response:
                raise Exception(f'Error is : {fee_response["error"]}')

            return utils.DEFAULT_SUGGESTED_TRANSACTION_FEE
    except:
        return utils.DEFAULT_SUGGESTED_TRANSACTION_FEE

async def get_unspent_transactions(haskoin_url, network, address):
    """Get unspent transactions

    :param haskoin_url: haskoin url
    :type haskoin_url: str
    :param network: network
    :type network: str
    :param address: The BCH address
    :type address: str
    :returns: The Bitcoin cash stats
    :raises: 'failed to query unspent transactions' if failed to query unspent transactions
    """
    try:
        account = await get_account(haskoin_url, network, address)

        api_url = f'{haskoin_url}/{to_haskoin_network(network)}/address/{address}/unspent?limit={account.txs}'

        client = http3.AsyncClient(timeout=5)
        response = await client.get(api_url)

        if response.status_code == 200:
            result = json.loads(response.content.decode('utf-8'))
            return result
        else:
            raise Exception('failed to query unspent transactions')
    except Exception as err:
      raise Exception(str(err))

# async def broadcast_tx(client_url, tx_hex):
#     """Broadcast transaction
#     https://sochain.com/api#send-transaction

#     :param client_url: The haskoin API url
#     :type client_url: str
#     :param tx_hex: tranaction hex
#     :type tx_hex: str
#     :returns: Transaction ID
#     """
#     try:
#         api_url = f'{client_url}/transactions'

#         client = http3.AsyncClient(timeout=5)
#         response = await client.post(url=api_url, data=tx_hex)

#         if response.status_code == 200:
#             res = json.loads(response.content.decode('utf-8'))['data']
#             return res['txid']
#         else:
#             return json.loads(response.content.decode('utf-8'))['data']
#     except Exception as err:
#         raise Exception(str(err))