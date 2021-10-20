# `xchainpy/xchainpy_bitcoin`

Bitcoin Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with bitcoinlib
- `models` - model wrapper for bitcoin required types
- `util` - Utitilies for using bitcoinlib and bitcoin chain

Following dependencies have to be installed into your project

```
bip_utils, bitcoinlib , http3 , xchainpy_client , xchainpy_crypto , xchainpy_util
```

## Service Providers

This package uses the following service providers:

| Function                    | Service     | Notes                                                                            |
| --------------------------- | ----------- | -------------------------------------------------------------------------------- |
| Balances                    | Sochain     | https://sochain.com/api#get-balance                                              |
| Transaction history         | Sochain     | https://sochain.com/api#get-display-data-address, https://sochain.com/api#get-tx |
| Transaction details by hash | Sochain     | https://sochain.com/api#get-tx                                                   |
| Transaction fees            | Bitgo       | https://app.bitgo.com/docs/#operation/v2.tx.getfeeestimate                       |
| Transaction broadcast       | Sochain     | https://sochain.com/api#send-transaction                                         |
| Explorer                    | Blockstream | https://blockstream.info                                                         |

Sochain API rate limits: https://sochain.com/api#rate-limits (300 requests/minute)


## Installation

```bash
pip install xchainpy_bitcoin
```

### Before install the package on M1 Mac, execute these commands:

```bash
brew install gmp openblas openssl autoconf automake libffi libtool pkg-config

CFLAGS=-I/opt/homebrew/opt/gmp/include LDFLAGS=-L/opt/homebrew/opt/gmp/lib pip3 install fastecdsa

CFLAGS=-I$(brew --prefix openssl)/include LDFLAGS=-L$(brew --prefix openssl)/lib pip3 install scrypt

export OPENBLAS="$(brew --prefix openblas) $OPENBLAS"
```


Bitcoin Client module
-----------------

**Initialize a client**

```python

from xchainpy_client.models.types import Network
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams

# Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoinClientParams(phrase=phrase, network=Network.Testnet))

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
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoinClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()
is_valid = client.validate_address(client.network, address) # bool
print(address)
print(is_valid)

# change index
address = client.get_address(1)
is_valid = client.validate_address(client.network, address) # bool
print(address)
print(is_valid)
```

**Fees**

```python

from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams

client = Client(BitcoinClientParams())

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
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoinClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()

balance = await client.get_balance(address=address)
balance = balance[0]

print(f'asset: {balance.asset}, amount: {balance.amount}')
```

**Transactions and Transaction_data**

```python
from xchainpy_client.models.tx_types import TxHistoryParams
from xchainpy_client.models.types import Network
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoinClientParams(phrase=phrase, network=Network.Testnet))

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
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams, BitcoinTxParams

phrase = 'atom green various power must another rent imitate gadget creek fat then'
client = Client(BitcoinClientParams(phrase=phrase, network=Network.Testnet))

address = client.get_address()

params = BitcoinTxParams(amount=0.0000001, recipient=address, memo='memo')
tx_hash = await client.transfer(params)

print(tx_hash)
```

**Explorer url**

```python
from xchainpy_client.models.types import Network
from xchainpy_bitcoin.client import Client
from xchainpy_bitcoin.models.client_types import BitcoinClientParams

client = Client(BitcoinClientParams())

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
$ python -m pytest xchainpy/xchainpy_bitcoin/tests
```

