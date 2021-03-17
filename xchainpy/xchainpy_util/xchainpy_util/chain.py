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
    return True if chain in chains else False