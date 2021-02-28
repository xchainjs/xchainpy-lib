# `xchainpy/xchain-binance`

Binance Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with binance_chain
- `models` - model wrapper for binance_chain types
- `util` - Utitilies for using binance_chain

Following dependencies have to be installed into your project

```
secp256k1 - python-binance-chain - binance-chain - pywallet - mnemonic
```


## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_binance/test/test_binance_clients.py
```

