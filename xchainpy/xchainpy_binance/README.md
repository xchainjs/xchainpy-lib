# `xchainpy/xchainpy_binance`

Binance Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with binance_chain
- `models` - model wrapper for binance_chain types
- `util` - Utitilies for using binance_chain

Following dependencies have to be installed into your project

```
secp256k1Crypto - py-binance-chain - pywallet - mnemonic
```

-----------

```bash
pip install xchainpy_binance
```


Binance Client module
-----------------

**Initialize a client**

```python

from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client

# Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Mainnet, phrase=phrase))

# if you want to change phrase after initialize the client
client.set_phrase('wheel leg dune emerge sudden badge rough shine convince poet doll kiwi sleep labor hello')

# if you want to change network after initialize the client
await client.purge_client()
client.set_network(Network.Mainnet)

# get python-binance-chain client
client.get_bnc_client()

# when you are done with the client, call this
await client.purge_client()
 ```
    


**Address methods**

```python

from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client

phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Mainnet, phrase=phrase))

address = client.get_address()

is_valid = client.validate_address(address) # bool

print(address)
print(is_valid)
```

**Fees**

```python

from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client

phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Mainnet, phrase=phrase))

fees = await client.get_fees()

multi_send_fees = await client.get_multi_send_fees()

single_and_multi_fees = await client.get_single_and_multi_fees()

print(f'''fees: 
average: {fees.average}
fast: {fees.fast}
fastest: {fees.fastest}\n''')

print(f'''multi_send_fees: 
average: {multi_send_fees.average}
fast: {multi_send_fees.fast}
fastest: {multi_send_fees.fastest}\n''')

print(f'''single_and_multi_fees: 
single:
    average: {single_and_multi_fees['single'].average}
    fast: {single_and_multi_fees['single'].fast}
    fastest: {single_and_multi_fees['single'].fastest}
multi:
    average: {single_and_multi_fees['single'].average}
    fast: {single_and_multi_fees['single'].fast}
    fastest: {single_and_multi_fees['single'].fastest}''')
```

**Balance**

```python

from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client

phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

address = client.get_address()

account = await client.get_account(adderss=address)

balances = await client.get_balance(address=address)

for balance in balances:
    print(f'asset: {balance.asset}, amount: {balance.amount}')
```

**Transactions and Transaction_data**

```python
from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client
from xchainpy_client.models.tx_types import TxHistoryParams


phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

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
from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client
from xchainpy_client.models.tx_types import TxParams
from xchainpy_util.asset import AssetBTC


phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

address = client.get_address()

params = TxParams(asset=AssetBNB, amount=0.0001, recipient=address, memo='memo')
tx_hash = await client.transfer(params)

print(tx_hash)
```

**Explorer url**

```python
from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client
from xchainpy_client.models.tx_types import TxParams


phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

print(client.get_explorer_url())
print(client.get_explorer_address_url('testAddressHere'))
print(client.get_explorer_tx_url('testTxHere'))

await client.purge_client()
client.set_network(Network.Mainnet)

print(client.get_explorer_url())
print(client.get_explorer_address_url('testAddressHere'))
print(client.get_explorer_tx_url('testTxHere'))
```

Crypto module
-----------------

```python
    from py_binance_chain.environment import BinanceEnvironment
    from xchainpy_binance import crypto

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    env = BinanceEnvironment.get_testnet_env()

    seed = crypto.mnemonic_to_seed(mnemonic=phrase)
    print(seed)

    private_key = crypto.mnemonic_to_private_key(mnemonic=phrase, index=0, env=env)
    print(private_key)

    public_key = crypto.private_key_to_public_key(private_key=private_key)
    print(public_key)

    address = crypto.private_key_to_address(private_key=private_key, prefix='tbnb')
    print(address)

    address = crypto.public_key_to_address(public_key=public_key, prefix='tbnb')
    print(address)

    is_valid = crypto.check_address(address=address, prefix='tbnb')
    print(is_valid)
```

## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_binance/tests
```

