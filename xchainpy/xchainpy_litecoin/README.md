# `xchainpy/xchain-litecoin`

Litecoin Module for XChainPy Clients

## Modules

- `client` - Custom client for communicating with bitcoinlib , sochain api
- `models` - Model wrapper for litecoin and sochain required types
- `util` - Utitilies for using bitcoinlib and sochain

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
| Transaction fees            | Bitgo       | https://app.bitgo.com/docs/#operation/v2.tx.getfeeestimate                       |
| Explorer                    | Blockstream | https://blockstream.info                                                         |
| Transaction broadcast       | Bitaps      | https://ltc.bitaps.com/broadcast                                                 |

Sochain API rate limits: https://sochain.com/api#rate-limits (300 requests/minute)

Bitgo API rate limits: https://app.bitgo.com/docs/#section/Rate-Limiting (10 requests/second)


## Tests

These packages needed to run tests:

- pytest `pip install pytest`
- pytest-asyncio `pip install pytest-asyncio`

How to run test ?

```bash
$ python -m pytest xchainpy/xchainpy_litecoin/test/test_litecoin_clients.py
```

