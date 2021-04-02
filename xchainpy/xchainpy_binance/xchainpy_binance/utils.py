from xchainpy_util.asset import Asset
from xchainpy_client.models.balance import Balance
from xchainpy_util.chain import BNBCHAIN
from xchainpy_client.models import tx_types
import datetime


def get_prefix(network):
    """Convert network type to prefix of address

    :param network: testnet or mainnet
    :type network: str
    :returns: tbnb or bnb
    """
    return 'tbnb' if network == 'testnet' else 'bnb'


def get_tx_type(tx_type: str):
    """Get tx type

    :param tx_type: type of transaction
    :type tx_type: str
    :returns: transfer or unknown
    """

    if tx_type == 'TRANSFER' or tx_type == 'DEPOSIT':
        return 'transfer'
    return 'unknown'


def parse_tx(tx):
    """Parse tx

    :param tx: The transaction to be parsed
    :type tx: str
    :returns: The transaction parsed from the binance tx
    """
    asset = Asset.from_str(f'BNB.{tx["txAsset"]}')
    tx_from = [tx_types.TxFrom(tx['fromAddr'], tx['value'])]
    tx_to = [tx_types.TxTo(tx['toAddr'], tx['value'])]
    tx_date = datetime.datetime.strptime(
        tx['timeStamp'], "%Y-%m-%dT%H:%M:%S.%fz")
    tx_type = get_tx_type(tx['txType'])
    tx_hash = tx['txHash']

    tx = tx_types.TX(asset, tx_from, tx_to, tx_date, tx_type, tx_hash)
    return tx
