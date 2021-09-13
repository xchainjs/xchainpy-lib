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
initialization of parameters for xchainpy_etheruem client
```
    prefix = "../xchainpy_ethereum/resources/testnet/"
    mnemonic = open(prefix + "mnemonic", 'r').readline()
``` 
web3 websocket provider is needed, e.g. infura
```
    wss = open(prefix + "infura", 'r').readline()
```
etherscan api is needed if there's intention to interact with non ERC20 token
the client will fetch abi for specific contract
```
    eth_api = open("../xchainpy_ethereum/resources/ether_api", 'r').readline()
    params = EthereumClientParams(wss_provider=wss, etherscan_token=eth_api, phrase=mnemonic)
```

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


