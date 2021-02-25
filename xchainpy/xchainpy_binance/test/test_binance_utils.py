import pytest
from xchainpy.xchainpy_binance import utils


class TestBinanceUtils:

    def test_get_prefix_testnet(self):
        assert utils.get_prefix('testnet') == 'tbnb'

    def test_get_prefix_mainnet(self):
        assert utils.get_prefix('mainnet') == 'bnb'

    def test_get_tx_type_transfer(self):
        assert utils.get_tx_type('TRANSFER') == 'transfer'

    def test_get_tx_type_deposit(self):
        assert utils.get_tx_type('DEPOSIT') == 'transfer'

    def test_get_tx_type_others(self):
        assert utils.get_tx_type('something') == 'unknown'

    def test_parse_tx(self):
        origin_tx = {
            'txHash': '0C6B721844BB5751311EC8910ED17F6E950E7F2D3D404145DBBA4E8B6428C3F1',
            'blockHeight': 123553830,
            'txType': 'TRANSFER',
            'timeStamp': '2020-11-03T17:21:34.152Z',
            'fromAddr': 'bnb1jxfh2g85q3v0tdq56fnevx6xcxtcnhtsmcu64m',
            'toAddr': 'bnb1c259wjqv38uqedhhufpz7haajqju0t5thass5v',
            'value': '4.97300000',
            'txAsset': 'USDT-6D8',
            'txFee': '0.00037500',
            'proposalId': None,
            'txAge': 58638,
            'orderId': None,
            'code': 0,
            'data': None,
            'confirmBlocks': 0,
            'memo': '',
            'source': 0,
            'sequence': 1034585,
        }
        tx = utils.parse_tx(origin_tx)
        assert tx.tx_from[0].address == origin_tx['fromAddr']
        assert tx.tx_to[0].address == origin_tx['toAddr']
