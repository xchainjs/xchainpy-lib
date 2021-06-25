from py_binance_chain.utils.segwit_addr import  decode_address, bech32_decode

HD_PATH = "m/44'/118'/0'/0/0"
DECODED_ADDRESS_LEN = 20

def check_address(address, prefix):
    """Checks whether an address is valid.

    :param address: the bech32 address to decode
    :type address: str
    :param prefix: bnb or tbnb
    :type prefix: str
    :returns: True or False
    """
    try:
        if not address.startswith(prefix):
            return False
        decoded_address = bech32_decode(address)
        decoded_address_length = len(decode_address(address))
        if decoded_address_length == DECODED_ADDRESS_LEN and decoded_address[0] == prefix:
            return True
    except:
        return False