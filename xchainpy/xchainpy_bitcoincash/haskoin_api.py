from typing import List
from xchainpy.xchainpy_bitcoincash import utils
from xchainpy.xchainpy_bitcoincash.models.api_types import AddressBalance, Block, Transaction, TransactionInput, TransactionOutput, TxUnspent
import http3
import json
import xchainpy.xchainpy_bitcoincash.models


async def get_account(client_url: str, address: str) -> AddressBalance:
    """Get account from address

    :param client_url: The haskoin API url
    :type client_url: str
    :param address: The BCH address
    :type address: str
    :returns: AddressBalance
    """
    try:
        api_url = f'{client_url}/address/{address}/balance'

        client = http3.AsyncClient()
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


async def get_transaction(client_url: str, tx_id: str) -> Transaction:
    """Get transaction by hash

    :param client_url: The haskoin API url
    :type client_url: str
    :param tx_id: The transaction id
    :type tx_id: str
    :returns: Transaction info
    :raises: 'failed to query transaction by a given hash' if failed to query transaction by a given hash
    """
    try:
        api_url = f'{client_url}/transaction/{tx_id}'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            balance_response = json.loads(response.content.decode('utf-8'))

            inputs = []
            for i in balance_response['inputs']:
                inputs.append(TransactionInput(i["pkscript"], i['value'], i['address'], i['witness'],
                                               i['sequence'], i['output'], i['sigscript'], i['coinbase'], i['txid']))
            outputs = []
            for i in balance_response['outputs']:
                outputs.append(TransactionOutput(
                    i["spent"], i['pkscript'], i['value'], i['address'], i['spender']))

            result = Transaction(balance_response["time"], balance_response["size"], inputs, balance_response["weight"], balance_response["fee"], balance_response["locktime"],
                                 balance_response["block"], outputs, balance_response["version"], balance_response["deleted"], balance_response["rbf"], balance_response["txid"])

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

        client = http3.AsyncClient()
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

async def get_unspent_transactions(client_url , address) -> List[TxUnspent]:
    """Get unspent transactions

    :param client_url: The haskoin API url
    :type client_url: str
    :param address: The BCH address
    :type address: str
    :returns: The Bitcoin cash stats
    :raises: 'failed to query unspent transactions' if failed to query unspent transactions
    """
    try:
        account = await get_account(client_url , address)

        api_url = f'{client_url}/address/{address}/unspent?limit={account.txs}'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            tx_response = json.loads(response.content.decode('utf-8'))
            result = [TxUnspent(i['pkscript'],i['value'],i['address'],Block(i['block']['height'] , i['block']['position']) ,i['index'],i['txid']) for i in tx_response]
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

#         client = http3.AsyncClient()
#         response = await client.post(url=api_url, data=tx_hex)

#         if response.status_code == 200:
#             res = json.loads(response.content.decode('utf-8'))['data']
#             return res['txid']
#         else:
#             return json.loads(response.content.decode('utf-8'))['data']
#     except Exception as err:
#         raise Exception(str(err))