# `xchainpy/xchainpy_ethereum`

Ethereum Module for XChainPy Clients

## Install
Python 3.8-3.9 tested
```angular2html
python setup.py install
```
you might need to include nimble in your path to install faster-than-requests, 
```angular2html
export PATH=/home/[username]/.nimble/bin:$PATH
pip install faster-than-requests --isolated --disable-pip-version-check --no-cache-dir --no-binary :all:
```
## Modules

- `client` - Custom client for communicating with ethereum-lib

Following dependencies have to be installed into your project

```
faster-than-requests==20.10.19
web3==5.16.0
websockets==8.1
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


