from bip_utils import Bip39MnemonicValidator


# Validate a mnemonic string by verifying its checksum
def validate_phrase(phrase: str):
    is_valid = Bip39MnemonicValidator(phrase).Validate()
    return is_valid