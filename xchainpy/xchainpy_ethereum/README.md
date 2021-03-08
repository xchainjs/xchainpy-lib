# `xchainpy/xchainpy_ethereum`

Ethereum Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with ethereum-lib

Following dependencies have to be installed into your project

```
ethereum-lib
```

## Service Providers

This package uses ``Infura WSS API``, head to https://infura.io/ to get your own websocket token.
In addition, if you want to interact with ``non-ERC20 token``, head to https://etherscan.io/ to get your
etherscan token.

Initialize mainnet client:

``
client = Client(phrase="mnemonimic", network="wss://mainnet.infura.io/ws/v3/...", network_type="mainnet",
                             ether_api="...")
``

Initialize ropsten(testnet) client:

``
client = Client(phrase="mnemonimic", network="wss://ropsten.infura.io/ws/v3/...", network_type="ropsten",
                             ether_api="...")
``

You can generate mnemonic phrase using ``crypto.py``, head to ``test/test_ropsten_client.py`` to see a
more comprehensive way to using this client.
## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

``Ropsten``
```bash
$ pytest test/test_ropsten_client.py
```
``Mainnet``
```bash
$ pytest test/test_mainnet_client.py
```


