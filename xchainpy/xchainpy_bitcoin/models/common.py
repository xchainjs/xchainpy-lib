class DerivePath:
    def __init__(self, index:int=0):

        self._mainnet = f"84'/0'/0'/0/{index}"
        self._testnet = f"84'/1'/0'/0/{index}"

    @property
    def mainnet(self):
        return self._mainnet

    @mainnet.setter
    def mainnet(self, mainnet):
        self._mainnet = mainnet

    @property
    def testnet(self):
        return self._testnet

    @testnet.setter
    def testnet(self, testnet):
        self._testnet = testnet


class UTXO:
    def __init__(self, hash : str , index : int , witness_utxo , tx_hex:str=None):
      self._hash = hash
      self._index = index
      self._witness_utxo = witness_utxo
      self._tx_hex = tx_hex

    @classmethod
    def from_sochain_utxo(cls, utxo):
        """Get utxo object from a sochain utxo

        :param utxo: sochain utxo
        :type utxo: dict
        :returns: UTXO object
        """
        hash = utxo['txid']
        index = utxo['output_no']
        value = int(float(utxo['value']) * 10 ** 8)
        script =  bytearray.fromhex(utxo['script_hex']) #utxo['script_hex']
        witness_utxo = Witness_UTXO(value, script)
        return UTXO(hash, index, witness_utxo)
    
    @property
    def hash(self):
        return self._hash

    @hash.setter
    def hash(self , hash):
        self._hash = hash
    
    @property
    def index(self):
        return self._index

    @index.setter
    def index(self , index):
        self._index = index

    @property
    def witness_utxo(self):
        return self._witness_utxo

    @witness_utxo.setter
    def witness_utxo(self , witness_utxo):
        self._witness_utxo = witness_utxo

    @property
    def tx_hex(self):
        return self._tx_hex

    @tx_hex.setter
    def tx_hex(self , tx_hex):
        self._tx_hex = tx_hex


class Witness_UTXO:
    def __init__(self, value, script):
      self._value = value
      self._script = script
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self , value):
        self._value = value
    
    @property
    def script(self):
        return self._script

    @script.setter
    def script(self , script):
        self._script = script