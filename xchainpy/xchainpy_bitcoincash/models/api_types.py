class AddressBalance:
    def __init__(self , received , utxo , address , txs , unconfirmed , confirmed):
        self._received = received
        self._utxo = utxo
        self._address = address
        self._txs = txs
        self._unconfirmed = unconfirmed
        self._confirmed = confirmed

    @property
    def received(self):
        return self._received

    @received.setter
    def received(self, received):
        self._received = received

    @property
    def utxo(self):
        return self._utxo

    @utxo.setter
    def utxo(self, utxo):
        self._utxo = utxo

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address
    
    @property
    def txs(self):
        return self._txs

    @txs.setter
    def txs(self, txs):
        self._txs = txs
        
    @property
    def unconfirmed(self):
        return self._unconfirmed

    @unconfirmed.setter
    def unconfirmed(self, unconfirmed):
        self._unconfirmed = unconfirmed

    @property
    def confirmed(self):
        return self._confirmed

    @confirmed.setter
    def confirmed(self, confirmed):
        self._confirmed = confirmed