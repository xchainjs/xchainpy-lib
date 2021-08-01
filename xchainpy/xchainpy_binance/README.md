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

.. code:: bash

    pip install xchainpy_binance


Binance Client
-----------------

**Initialize a client**

.. code:: python

    from xchainpy_client.models.types import Network, XChainClientParams
    from xchainpy_binance.client import Client

    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    client = Client(XChainClientParams(network=Network.Mainnet, phrase=phrase))

    # if you want to change phrase after initialize the client
    client.set_phrase('wheel leg dune emerge sudden badge rough shine convince poet doll kiwi sleep labor hello')

    # if you want to change network after initialize the client
    client.set_network(Network.Mainnet)

    # get python-binance-chain client
    client.get_bnc_client()

    # when you are done with the client, call this.
    await client.purge_client()
    


**Address methods**

.. code:: python

    from xchainpy_client.models.types import Network, XChainClientParams
    from xchainpy_binance.client import Client

    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    client = Client(XChainClientParams(network=Network.Mainnet, phrase=phrase))

    address = client.get_address()

    is_valid = client.validate_address(address) # bool

    print(address)
    print(is_valid)

**Fees**

.. code:: python

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

**Balance**

.. code:: python

    from xchainpy_client.models.types import Network, XChainClientParams
    from .client import Client

    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

    address = client.get_address()

    balances = await client.get_balance(address=address)

    for balance in balances:
        print(f'asset: {balance.asset}, amount: {balance.amount}')

**Transactions and Transaction_data**

.. code:: python

    from xchainpy_client.models.types import Network, XChainClientParams
    from .client import Client

    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    client = Client(XChainClientParams(network=Network.Testnet, phrase=phrase))

    address = client.get_address()

    balances = await client.get_balance(address=address)

    for balance in balances:
        print(f'asset: {balance.asset}, amount: {balance.amount}')

## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_binance/tests/test_binance_clients.py
```

