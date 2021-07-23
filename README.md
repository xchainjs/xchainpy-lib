# xchainpy-lib
XChainPY is a library with a common interface for multiple blockchains, built for simple and fast integration for wallets and more.

Join the conversation!
https://t.me/xchainpy

## XChainPY uses following libraries, frameworks and more:

- [bitcoinlib](https://github.com/1200wd/bitcoinlib)
- [python-binance-chain](https://github.com/sammchardy/python-binance-chain)
- [web3.py](https://github.com/ethereum/web3.py)
- [bitcash](https://github.com/pybitcash/bitcash)

# Interface

### Common Interface

The interface supports as a minimum the following functions for each blockchain:

1. Initialise with a valid BIP39 phrase and specified network (testnet/mainnet)
2. Get the address, with support for BIP44 path derivations (default is Index 0)
3. Get the balance (UTXO or account-based)
4. Get transaction history for that address
5. Make a simple transfer
6. Get blockchain fee information (standard, fast, fastest)

### Extended Interface

Some blockchains have different functions. More advanced logic can be built by extending the interface, such as for Binance Chain and Cosmos chains.

### Return the Client

For wallets that need even more flexibility (smart contract blockchains) the client can be retrieved and the wallet is then free to handle directly.

## License

MIT [XChainPY](https://github.com/xchainjs/xchainpy-lib)