from xchainpy.xchainpy_util.asset import Asset

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
    def __init__(self, asset: Asset, tx_from: TxFrom, tx_to: TxTo, tx_date, tx_type, tx_hash):
        self._asset = asset
        self._tx_from = tx_from
        self._tx_to = tx_to
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