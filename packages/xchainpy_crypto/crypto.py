from bip_utils import Bip39MnemonicValidator


# Validate a mnemonic string by verifying its checksum
def validatePhrase(self, phrase: str):
    is_valid = Bip39MnemonicValidator(phrase).Validate()
    return is_valid
