from secp256k1 import PrivateKey
from mnemonic import Mnemonic
# from pywallet.utils.bip32 import Wallet as Bip32Wallet
from py_binance_chain.utils.segwit_addr import address_from_public_key, decode_address, bech32_decode
from py_binance_chain.environment import BinanceEnvironment
from py_binance_chain.wallet import Wallet

HD_PATH = "44'/714'/0'/0/0"
DECODED_ADDRESS_LEN = 20

def mnemonic_to_seed(mnemonic, pass_phrase = ''):
    """Convert mnemonic (phrase) to seed

    :param mnemonic: A phrase
    :type mnemonic: str
    :param pass_phrase: A password
    :type pass_phrase: str
    :returns: seed
    """
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic, pass_phrase)
    return seed

def mnemonic_to_private_key(mnemonic, env, pass_phrase = ''):
    """Convert mnemonic (phrase) to a private key

    :param mnemonic: A phrase
    :type mnemonic: str
    :param pass_phrase: A password
    :type pass_phrase: str
    :returns: private key
    """
    wallet = Wallet.create_wallet_from_mnemonic(mnemonic, env)
    private_key = wallet.private_key
    return private_key

def private_key_to_public_key(private_key):
    """Convert a private key to a public key

    :param private_key
    :type private_key: str
    :returns: public key
    """
    pk = PrivateKey(bytes(bytearray.fromhex(private_key)))
    public_key = pk.pubkey.serialize(compressed=True)
    return public_key

def private_key_to_address(private_key, prefix):
    """Convert a private key to an address

    :param private_key
    :type private_key: str
    :param prefix: (bnb or tbnb)
    :type prefix: str
    :returns: address
    """
    public_key = private_key_to_public_key(private_key)
    address = address_from_public_key(public_key, prefix)
    return address

def public_key_to_address(public_key, prefix):
    """Convert a public key to an address

    :param public_key
    :type public_key: bytes
    :param prefix: (bnb or tbnb)
    :type prefix: str
    :returns: address
    """
    address = address_from_public_key(public_key, prefix)
    return address

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