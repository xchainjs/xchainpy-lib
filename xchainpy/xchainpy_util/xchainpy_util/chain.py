import enum
class Chain(enum.Enum):
    Binance = "BNB"
    Bitcoin = "BTC"
    Ethereum = "ETH"
    THORChain = "THOR"
    Cosmos = "GAIA"
    Polkadot = "POLKA"
    BitcoinCash = "BCH"
    Litecoin = "LTC"

BNBCHAIN = "BNB"
BTCCHAIN = "BTC"
ETHCHAIN = "ETH"
THORCHAIN = "THOR"
COSMOSCHAIN = "GAIA"
POLKADOTCHAIN = "POLKA"
BITCOINCASH = "BCH"
LTCCHAIN = "LTC"

chains = ["BNB", "BTC", "ETH", "THOR", "GAIA", "POLKA", "BCH", "LTC"]

def is_chain(chain):
    """Is the argument a chain or not
    :returns: True of False
    """
    if chain in chains or isinstance(chain, Chain):
        return True
    return False