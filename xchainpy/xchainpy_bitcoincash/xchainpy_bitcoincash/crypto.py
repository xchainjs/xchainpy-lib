from .utils import get_derive_path
from mnemonic.mnemonic import Mnemonic
import binascii
from bip_utils import Bip32, Bip32Utils

from bitcash import Key, PrivateKeyTestnet

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

def mnemonic_to_private_key(mnemonic,network, pass_phrase = ''):
    """Convert mnemonic (phrase) to a private key

    :param mnemonic: A phrase
    :type mnemonic: str
    :param network: testnet or mainnet
    :type mnemonic: str
    :param pass_phrase: A password
    :type pass_phrase: str
    :returns: private key
    """    
    seed = mnemonic_to_seed(mnemonic, pass_phrase)
    bip32_ctx = Bip32.FromSeed(seed)
    HD_PATH = get_derive_path().testnet if network == "testnet" else get_derive_path().mainnet
    hd_path = HD_PATH[2:]

    bip32_ctx = bip32_ctx.DerivePath(hd_path)
    priv_key = bip32_ctx.PrivateKey().Raw().ToHex()
    return priv_key
    

def private_key_to_address(priv_key, network):
    """Convert a private key to an address

    :param priv_key
    :type public_key: hex
    """
    KeyClass = PrivateKeyTestnet if network == "testnet" else Key
    key = KeyClass.from_hex(priv_key)
    return key.address