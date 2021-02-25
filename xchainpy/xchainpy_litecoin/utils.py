from bitcoinlib.keys import Address


def validate_address(network, address):
    """Validate the LTC address

    :param network: testnet or mainnet
    :type network: str
    :param address: address
    :type address: str
    :returns: True or False
    """
    try:
        address = Address.import_address(address=address, network=(
            'litecoin' if network == 'mainnet' else 'litecoin_testnet'))
        return True
    except:
        return False

def network_to_bitcoinlib_format(network: str):
    return 'litecoin' if network == 'mainnet' else 'litecoin_testnet'
