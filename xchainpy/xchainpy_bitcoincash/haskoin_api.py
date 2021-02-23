from xchainpy.xchainpy_bitcoincash.utils import DEFAULT_SUGGESTED_TRANSACTION_FEE
from xchainpy.xchainpy_bitcoincash.models.api_types import AddressBalance, Transaction, TransactionInput, TransactionOutput
import http3
import json
import xchainpy.xchainpy_bitcoincash.models


async def get_account(client_url: str, address: str) -> AddressBalance:
    """Get address balance
    https://api.haskoin.com/#/Address/getBalance
    :param client_url: haskoin mainnet or testnet
    :type client_url: str
    :param address: wallet address
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
            balance_response = json.loads(response.content.decode('utf-8'))
            if "error" in balance_response:
                raise Exception(
                    f'Error is : {balance_response["error"]}\nMessage is : {balance_response["message"]}')
            else:
                return None
    except Exception as err:
        raise Exception(str(err))


async def get_suggested_tx_fee():
    try:
        api_url = 'https://app.bitgo.com/api/v2/bch/tx/fee'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            fee_response = json.loads(response.content.decode('utf-8'))
            return fee_response["feePerKb"] / 1000
        else:
            fee_response = json.loads(response.content.decode('utf-8'))
            if "error" in fee_response:
                raise Exception(f'Error is : {fee_response["error"]}')
            else:
                return None
    except Exception as err:
        # raise Exception(str(err))
        return DEFAULT_SUGGESTED_TRANSACTION_FEE
