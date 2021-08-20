import json
import http3

BITCORE_URL = 'https://api.bitcore.io/api/BCH'

async def broadcast_tx(network, tx_hex):
    """Broadcast transaction

    :param network: testnet or mainnet
    :type network: str
    :param tx_hex: tranaction hex
    :type tx_hex: str
    :returns: Transaction ID
    """
    try:
        api_url = f'{BITCORE_URL}/{network}/tx/send'


        client = http3.AsyncClient(timeout=5)
        data = {
            'rawTx': tx_hex,
            'network': network,
            'coin': 'BCH'            
        }
        response = await client.post(url=api_url, json=data)

        if response.status_code == 200:
            res = json.loads(response.content.decode('utf-8'))['txid']
            return res
        else:
            raise Exception(response.content.decode('utf-8'))
    except Exception as err:
        raise Exception(str(err))