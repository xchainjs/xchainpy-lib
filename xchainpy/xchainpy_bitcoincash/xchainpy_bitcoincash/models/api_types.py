import bitcash
from bitcash.network.meta import Unspent


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

class TransactionInput:
    def __init__(self , pkscript , value , address , witness , sequence , output , sigscript , coinbase , txid):
        self._pkscript = pkscript
        self._value = value
        self._address = address
        self._witness = witness
        self._sequence = sequence
        self._output = output
        self._sigscript = sigscript
        self._coinbase = coinbase
        self._txid = txid
    
    @property
    def pkscript(self):
        return self._pkscript

    @pkscript.setter
    def pkscript(self, pkscript):
        self._pkscript = pkscript 
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value 

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address 

    @property
    def witness(self):
        return self._witness

    @witness.setter
    def witness(self, witness):
        self._witness = witness 

    @property
    def sequence(self):
        return self._sequence

    @sequence.setter
    def sequence(self, sequence):
        self._sequence = sequence 
    
    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, output):
        self._output = output 

    @property
    def sigscript(self):
        return self._sigscript

    @sigscript.setter
    def sigscript(self, sigscript):
        self._sigscript = sigscript 

    @property
    def coinbase(self):
        return self._coinbase

    @coinbase.setter
    def coinbase(self, coinbase):
        self._coinbase = coinbase 

    @property
    def txid(self):
        return self._txid

    @txid.setter
    def txid(self, txid):
        self._txid = txid 

class TransactionOutput:
    def __init__(self ,spent , pkscript , value , address , spender):
        self._spent = spent
        self._pkscript = pkscript
        self._value = value
        self._address = address
        self._spender = spender
    
    @property
    def spent(self):
        return self._spent

    @spent.setter
    def spent(self, spent):
        self._spent = spent 

    @property
    def pkscript(self):
        return self._pkscript

    @pkscript.setter
    def pkscript(self, pkscript):
        self._pkscript = pkscript 
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value 
    
    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def spender(self):
        return self._spender

    @spender.setter
    def spender(self, spender):
        self._spender = spender


class Transaction:
    def __init__(self , time , size , inputs : TransactionInput , weight , fee , locktime , block , outputs : TransactionOutput , version , deleted , rbf , txid):
        self._time = time
        self._size = size
        self._inputs = inputs
        self._weight = weight
        self._fee = fee
        self._locktime = locktime
        self._block = block
        self._outputs = outputs
        self._version = version
        self._deleted = deleted
        self._rbf = rbf
        self._txid = txid
        
    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        self._time = time 

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, inputs):
        self._inputs = inputs

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, weight):
        self._weight = weight

    @property
    def fee(self):
        return self._fee

    @fee.setter
    def fee(self, fee):
        self._fee = fee

    @property
    def locktime(self):
        return self._locktime

    @locktime.setter
    def locktime(self, locktime):
        self._locktime = locktime
    
    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block):
        self._block = block

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, outputs):
        self._outputs = outputs

    @property
    def version(self):
        return self._outputs

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def deleted(self):
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        self._deleted = deleted

    @property
    def rbf(self):
        return self._rbf

    @rbf.setter
    def rbf(self, rbf):
        self._rbf = rbf

    @property
    def txid(self):
        return self._txid

    @txid.setter
    def txid(self, txid):
        self._txid = txid

class Block:
    def __init__(self , height , position):
        self._height = height
        self._position = position
    
    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, height):
        self._height = height

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

class TxUnspent:
    def __init__(self, pkscript, value, address, block:Block, index, txid):
        self._pkscript = pkscript
        self._value = value
        self._address = address
        self._block = block
        self._index = index
        self._txid = txid

    @classmethod
    def unspent_from_object(cls , unspent):
        txid = unspent['txid']
        output_index = unspent['index']
        script = bytes.fromhex(unspent['pkscript'])
        satoshis = unspent['value']
        return Unspent(satoshis, 0, script, txid, output_index)

    @property
    def pkscript(self):
        return self._pkscript

    @pkscript.setter
    def pkscript(self, pkscript):
        self._pkscript = pkscript

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def block(self):
        return self._block

    @block.setter
    def block(self, block):
        self._block = block

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        self._index = index

    @property
    def txid(self):
        return self._txid

    @txid.setter
    def txid(self, txid):
        self._txid = txid