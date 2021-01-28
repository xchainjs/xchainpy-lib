from bip_utils import Bip39MnemonicValidator


# Validate a mnemonic string by verifying its checksum
def validate_phrase(phrase: str):
    """Check validity of mnemonic (phrase)

    :param phrase: a phrase
    :type phrase: str
    :returns: is the phrase valid or not (true or false)
    """
    is_valid = Bip39MnemonicValidator(phrase).Validate()
    return is_valid