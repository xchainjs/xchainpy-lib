from xchainpy.xchainpy_bitcoincash.models.api_types import AddressBalance
import http3
import json
import xchainpy.xchainpy_bitcoincash.models.

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
            return balance_response
        else:
            return None
    except Exception as err:
        raise Exception(str(err))