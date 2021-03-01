# `xchainpy/xchainpy_bitcoin`

Bitcoin Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with bitcoinlib
- `models` - model wrapper for bitcoin required types
- `util` - Utitilies for using bitcoinlib and bitcoin chain

Following dependencies have to be installed into your project

```
bitcoinlib
```

## Service Providers

This package uses the following service providers:

| Function                    | Service     | Notes                                                                            |
| --------------------------- | ----------- | -------------------------------------------------------------------------------- |
| Balances                    | Sochain     | https://sochain.com/api#get-balance                                              |
| Transaction history         | Sochain     | https://sochain.com/api#get-display-data-address, https://sochain.com/api#get-tx |
| Transaction details by hash | Sochain     | https://sochain.com/api#get-tx                                                   |
| Transaction fees            | bitcoinfees | https://bitcoinfees.earn.com/api/v1/fees/recommended                             |
| Transaction broadcast       | Sochain     | https://sochain.com/api#send-transaction                                         |
| Explorer                    | Blockstream | https://blockstream.info                                                         |

Sochain API rate limits: https://sochain.com/api#rate-limits (300 requests/minute)


## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_bitcoin/test/test_bitcoin_clients.py
```

