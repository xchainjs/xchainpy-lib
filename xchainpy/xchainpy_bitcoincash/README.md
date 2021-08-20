# `xchainpy/xchain-bitcoincash`

Bitcoin-Cash Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with bitcash , haskoin api
- `models` - Model wrapper for bitcoin-cash and haskoin required types
- `util` - Utitilies for using bitcash and haskoin

Following dependencies have to be installed into your project

```
bitcash - cashaddress - mnemonic - bip_utils
```

## Service Providers

This package uses the following service providers:

| Function                    | Service       | Notes                                                                            |
| --------------------------- | ------------- | -------------------------------------------------------------------------------- |
| Balances                    | Haskoin       | https://api.haskoin.com/#/Address/getBalance                                     |
| Transaction history         | Haskoin       | https://api.haskoin.com/#/Address/getAddressTxsFull                              |
| Transaction details by hash | Haskoin       | https://api.haskoin.com/#/Transaction/Transaction                                |
| Transaction fees            | Bitgo         | https://app.bitgo.com/docs/#operation/v2.tx.getfeeestimate                       |
| Explorer                    | Blockchain.com| https://www.blockchain.com                                                       |

Haskoin API rate limits: No

Bitgo API rate limits: https://app.bitgo.com/docs/#section/Rate-Limiting (10 requests/second)


Bitcoincash Client module
-----------------

**Initialize a client**

```python

from xchainpy_client.models.types import Network
from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams

# Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoincashClientParams(phrase=phrase, network=Network.Testnet))

# if you want to change phrase after initialize the client
client.set_phrase('caution pear excite vicious exotic slow elite marble attend science strategy rude')

# if you want to change network after initialize the client
client.purge_client()
client.set_network(Network.Mainnet)

# when you are done with the client, call this
client.purge_client()
 ```
    


**Address methods**

```python

from xchainpy_client.models.types import Network
from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoincashClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()
is_valid = client.validate_address(address) # bool
print(address)
print(is_valid)

# change index
address = client.get_address(1)
is_valid = client.validate_address(address) # bool
print(address)
print(is_valid)
```

**Fees**

```python

from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams

client = Client(BitcoincashClientParams())

# Get feeRate estimations
fee_rates = await client.get_fee_rates()

# Get fee estimations
fees = await client.get_fees()

# Get fee estimations with memo
memo = 'SWAP:THOR.RUNE'
fees_with_memo = await client.get_fees(memo)


print(f'''fee rates: 
average: {fee_rates.average}
fast: {fee_rates.fast}
fastest: {fee_rates.fastest}\n''')

print(f'''fees: 
average: {fees.average}
fast: {fees.fast}
fastest: {fees.fastest}\n''')

print(f'''fees with memo: 
average: {fees_with_memo.average}
fast: {fees_with_memo.fast}
fastest: {fees_with_memo.fastest}\n''')
```

**Balance**

```python

from xchainpy_client.models.types import Network
from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoincashClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()

balance = await client.get_balance(address=address)
balance = balance[0]

print(f'asset: {balance.asset}, amount: {balance.amount}')
```

**Transactions and Transaction_data**

```python
from xchainpy_client.models.tx_types import TxHistoryParams
from xchainpy_client.models.types import Network
from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoincashClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()

params = TxHistoryParams(address=address, limit=1)
transactions = await client.get_transactions(params)
# type of transactions is xchainpy_client.models.tx_types.TxPage

t = transactions.txs[0]
print(t.asset)
print(t.tx_from[0].amount)
print(t.tx_from[0].address)
print(t.tx_to[0].amount)
print(t.tx_to[0].address)
print(t.tx_date)
print(t.tx_type)
print(t.tx_hash)

transaction = await client.get_transaction_data(t.tx_hash)
# transaction object is equal by t object
```

**Transfer**

```python
from xchainpy_client.models.types import Network
from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams, BitcoincashTxParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoincashClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()

params = BitcoincashTxParams(amount=0.0000001, recipient=address, memo='memo')
tx_hash = await client.transfer(params)

print(tx_hash)
```

**Explorer url**

```python
from xchainpy_client.models.types import Network
from xchainpy_bitcoincash.client import Client
from xchainpy_bitcoincash.models.client_types import BitcoincashClientParams

client = Client(BitcoincashClientParams())

print(client.get_explorer_url())
print(client.get_explorer_address_url('testAddressHere'))
print(client.get_explorer_tx_url('testTxHere'))

client.purge_client()
client.set_network(Network.Mainnet)

print(client.get_explorer_url())
print(client.get_explorer_address_url('testAddressHere'))
print(client.get_explorer_tx_url('testTxHere'))
```



## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_bitcoincash/tests
```

