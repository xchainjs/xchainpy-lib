# `xchainpy/xchainpy_ethereum`

Ethereum Module for XChainPy Clients

## Environment
tested with Python Virtual Environment 3.8 3.9

## Installation
```angular2html
python3 setup.py install
```

## Service Providers
- ``Infura WSS API`` was used to interact with ethereum blockchain, head to https://infura.io/ to get your own websocket token.
- If interaction with ``non-ERC20 token`` is needed, head to https://etherscan.io/ to get your etherscan token.

## Initialization of Client
Pass in your infura WSS api token as network, and pass your ether token as ether_api (not enforced).


- Initialize mainnet client:
``
client = Client(phrase="mnemonimic", network="wss://mainnet.infura.io/ws/v3/...", network_type="mainnet",
                             ether_api="...")
``

- Initialize ropsten(testnet) client:
``
client = Client(phrase="mnemonimic", network="wss://ropsten.infura.io/ws/v3/...", network_type="ropsten",
                             ether_api="...")
``

Head to ``test/test_ropsten_client.py`` to see a
more comprehensive way to using this client.
## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```angular2html
cd test/
```
``Ropsten``
```bash
$ pytest test_ropsten_client.py
```
``Mainnet``
```bash
$ pytest test_mainnet_client.py
```


