from typing import List
from xchainpy_util.asset import Asset

class TxFrom:
    def __init__(self, address, amount):
        self._address = address
        self._amount = amount

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address


    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

class TxTo:
    def __init__(self, address, amount):
        self._address = address
        self._amount = amount

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address


    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

class TX:
    def __init__(self, asset: Asset, tx_froms, tx_tos, tx_date, tx_type:str, tx_hash:str):
        self._asset = asset
        self._tx_from = tx_froms # list of "to" txs. BNC will have one `TxFrom` only, `BTC` might have many transactions going "in" (based on UTXO)
        self._tx_to = tx_tos # list of "to" transactions. BNC will have one `TxTo` only, `BTC` might have many transactions going "out" (based on UTXO)
        self._tx_date = tx_date
        self._tx_type = tx_type
        self._tx_hash = tx_hash

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset):
        self._asset = asset

    @property
    def tx_from(self):
        return self._tx_from

    @tx_from.setter
    def tx_from(self, tx_from):
        self._tx_from = tx_from

    @property
    def tx_to(self):
        return self._tx_to

    @tx_to.setter
    def tx_to(self, tx_to):
        self._tx_to = tx_to

    @property
    def tx_date(self):
        return self._tx_date

    @tx_date.setter
    def tx_date(self, tx_date):
        self._tx_date = tx_date

    @property
    def tx_type(self):
        return self._tx_type

    @tx_type.setter
    def tx_type(self, tx_type):
        self._tx_type = tx_type

    @property
    def tx_hash(self):
        return self._tx_hash

    @tx_hash.setter
    def tx_hash(self, tx_hash):
        self._tx_hash = tx_hash

class TxHistoryParams:
    def __init__(self, address:str, offset:int=None, limit:int=None, start_time=None, asset:Asset=None):
        self._address = address
        self._offset = offset
        self._limit = limit
        self._start_time = start_time
        self._asset = asset

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address


    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        self._offset = offset

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        self._limit = limit

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        self._start_time = start_time

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset):
        self._asset = asset

class TxParams:
    def __init__(self, asset:Asset, amount, recipient, memo='', wallet_index=None):
        self._asset = asset
        self._amount = amount
        self._recipient = recipient
        self._memo = memo
        self._wallet_index = wallet_index

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, asset):
        self._asset = asset

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = amount

    @property
    def recipient(self):
        return self._recipient

    @recipient.setter
    def recipient(self, recipient):
        self._recipient = recipient

    @property
    def memo(self):
        return self._memo

    @memo.setter
    def memo(self, memo):
        self._memo = memo

    @property
    def wallet_index(self):
        return self._wallet_index

    @wallet_index.setter
    def wallet_index(self, wallet_index):
        self._wallet_index = wallet_index

class TxPage:
    def __init__(self, total:int, txs:List[TX]):
        self._total = total
        self._txs = txs

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, total):
        self._total = total

    @property
    def txs(self):
        return self._txs

    @txs.setter
    def txs(self, txs):
        self._txs = txs