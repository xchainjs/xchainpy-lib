import json
import http3


async def broadcast_tx(blockstream_url, network, tx_hex):
    """Broadcast transaction
    https://github.com/Blockstream/esplora/blob/master/API.md#post-tx

    :param blockstream_url: blockstream url
    :type blockstream_url: str
    :param network: testnet or mainnet
    :type network: str
    :param tx_hex: tranaction hex
    :type tx_hex: str
    :returns: Transaction ID
    """
    try:
        if network == 'testnet':
            api_url = f'{blockstream_url}/testnet/api/tx'
        else:
            api_url = f'{blockstream_url}/api/tx'

        client = http3.AsyncClient(timeout=5)
        response = await client.post(url=api_url, data=tx_hex)

        if response.status_code == 200:
            res = str(response.content.decode('utf-8'))
            return res
        else:
            raise Exception(str(response.content.decode('utf-8')))
    except Exception as err:
        raise Exception(str(err))