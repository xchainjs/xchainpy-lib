from bitcash.format import bytes_to_wif
from bitcash.wallet import wif_to_key
from bitcoinlib.wallets import Wallet
from secp256k1 import PrivateKey
from xchainpy.xchainpy_bitcoincash.utils import get_derive_path
from mnemonic.mnemonic import Mnemonic
from pywallet.utils.bip32 import Wallet as Bip32Wallet
from bitcash import Key

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
    wallet = Bip32Wallet.from_master_secret(seed=seed, network='BCH')
    HD_PATH = get_derive_path().testnet if network == "testnet" else get_derive_path().mainnet
    child = wallet.get_child_for_path(HD_PATH)
    private_key = child.get_private_key_hex()
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

def private_key_to_address(priv_key):
    """Convert a private key to an address

    :param priv_key
    :type public_key: hex
    """
    key = Key.from_hex(priv_key)
    return key.address