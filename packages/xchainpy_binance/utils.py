def get_prefix(network):
    """Convert network type to prefix of address

    :param network: testnet or mainnet
    :type network: str
    :returns: tbnb or bnb
    """
    return 'tbnb' if network == 'testnet' else 'bnb'