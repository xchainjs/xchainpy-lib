from secp256k1 import PrivateKey
from mnemonic import Mnemonic
from pywallet.utils.bip32 import Wallet as Bip32Wallet
from binance_chain.utils.segwit_addr import address_from_public_key, decode_address
from binance_chain.environment import BinanceEnvironment

def mnemonicToSeed(mnemonic, passPhrase = ''):
    mnemo = Mnemonic("english")
    seed = mnemo.to_seed(mnemonic, passPhrase)
    return seed

