from secp256k1 import PrivateKey
from mnemonic import Mnemonic
from pywallet.utils.bip32 import Wallet as Bip32Wallet
from binance_chain.utils.segwit_addr import address_from_public_key, decode_address
from binance_chain.environment import BinanceEnvironment

HD_PATH = "44'/714'/0'/0/0"

def mnemonic_to_seed(mnemonic, pass_phrase = ''):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic, pass_phrase)
    return seed

def mnemonic_to_private_key(mnemonic, pass_phrase = ''):
    seed = mnemonic_to_seed(mnemonic, pass_phrase)
    wallet = Bip32Wallet.from_master_secret(seed=seed, network='BTC')
    child = wallet.get_child_for_path(HD_PATH)
    private_key = child.get_private_key_hex().decode()
    return private_key

def private_key_to_public_key(private_key):
    pk = PrivateKey(bytes(bytearray.fromhex(private_key)))
    public_key = pk.pubkey.serialize(compressed=True)
    return public_key

def private_key_to_address(private_key, prefix):
    public_key = private_key_to_public_key(private_key)
    address = address_from_public_key(public_key, prefix)
    return address

def public_key_to_address(public_key, prefix):
    address = address_from_public_key(public_key, prefix)
    return address