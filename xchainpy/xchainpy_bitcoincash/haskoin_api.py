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
                raise Exception(f'Error is : {balance_response["error"]}\nMessage is : {balance_response["message"]}')
            else:
                result = AddressBalance(balance_response['received'],balance_response['utxo'],balance_response['address'],balance_response['txs'],balance_response['unconfirmed'],balance_response['confirmed'])
                return result
        else:
            return None
    except Exception as err:
        raise Exception(str(err))

async def get_transaction(client_url : str , tx_id : str) -> Transaction :
    try:
        api_url = f'{client_url}/transaction/{tx_id}'

        client = http3.AsyncClient()
        response = await client.get(api_url)

        if response.status_code == 200:
            balance_response = json.loads(response.content.decode('utf-8'))
            result = Transaction(balance_response["time"],balance_response["size"],
            TransactionInput(balance_response["inputs"]["pkscript"],balance_response["inputs"]["value"],balance_response["inputs"]["address"],balance_response["inputs"]["witness"],
            balance_response["inputs"]["sequence"],balance_response["inputs"]["output"],balance_response["inputs"]["sigscript"],balance_response["inputs"]["coinbase"],balance_response["inputs"]["txid"]),
            balance_response["weight"],balance_response["fee"],balance_response["locktime"],balance_response["block"],
            TransactionOutput(balance_response["outputs"]["spent"],balance_response["outputs"]["pkscript"],balance_response["outputs"]["value"],balance_response["outputs"]["address"],balance_response["outputs"]["spender"]),
            balance_response["version"],balance_response["deleted"],balance_response["rbf"],balance_response["txid"])

            return result
        else:
            balance_response = json.loads(response.content.decode('utf-8'))
            if "error" in balance_response:
                raise Exception(f'Error is : {balance_response["error"]}\nMessage is : {balance_response["message"]}')
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