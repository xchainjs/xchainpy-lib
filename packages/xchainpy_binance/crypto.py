from secp256k1 import PrivateKey
from mnemonic import Mnemonic
from pywallet.utils.bip32 import Wallet as Bip32Wallet
from binance_chain.utils.segwit_addr import address_from_public_key, decode_address
from binance_chain.environment import BinanceEnvironment

HD_PATH = "44'/714'/0'/0/0"

def mnemonicToSeed(mnemonic, passPhrase = ''):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic, passPhrase)
    return seed

def mnemonicToPrivateKey(mnemonic, passPhrase = ''):
    seed = mnemonicToSeed(mnemonic, passPhrase)
    wallet = Bip32Wallet.from_master_secret(seed=seed, network='BTC')
    child = wallet.get_child_for_path(HD_PATH)
    privateKey = child.get_private_key_hex().decode()
    return privateKey

def privateKeyToPublicKey(privateKey):
    pk = PrivateKey(bytes(bytearray.fromhex(privateKey)))
    publicKey = pk.pubkey.serialize(compressed=True)
    return publicKey

def privateKeyToAddress(privateKey, network):
    publicKey = privateKeyToPublicKey(privateKey)
    address = address_from_public_key(publicKey, network.hrp)
    return address

def publicKeyToAddress(publicKey, network):
    address = address_from_public_key(publicKey, network.hrp)
    return address