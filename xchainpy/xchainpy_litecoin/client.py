from xchainpy.xchainpy_client.interface import IXChainClient
from xchainpy.xchainpy_crypto.crypto import validate_phrase
from xchainpy.xchainpy_litecoin import utils

from bitcoinlib.wallets import Wallet, wallet_delete_if_exists


class ILiteCoinClient():
    def derive_path(self):
        pass

    def get_fees_with_rates(self):
        pass

    def get_fees_with_memo(self):
        pass

    def get_fee_rates(self):
        pass


class Client(ILiteCoinClient, IXChainClient):

    def __init__(self, phrase: str, network='testnet', sochain_url=None, bitaps_url=None):
        self.set_network(network)
        self.set_sochain_url(sochain_url or self.get_default_sochain_url())
        self.set_bitaps_url(bitaps_url or self.get_default_bitaps_url())
        self.set_phrase(phrase)

    def set_network(self, network: str):
        """Set/update the current network

        :param network: mainnet or testnet
        :type network: str
        :raises: Network must be provided if network has not been set before
        :raises: `Invalid network' if the given network is invalid
        """
        if not network:
            raise Exception("Network must be provided")
        if not network in ['testnet', 'mainnet']:
            raise Exception('Invalid network')
        else:
            self.network = 'litecoin_testnet' if network == 'testnet' else 'litecoin'

    def set_wallet(self, phrase):
        """Set/update the current wallet

        :param phrase: A new phrase
        :type phrase: str
        :returns: the wallet
        """
        # self.wallet = Wallet("Wallet")
        wallet_delete_if_exists('Wallet', force=True)
        self.wallet = Wallet.create(
            "Wallet", keys=self.phrase, witness_type='segwit', network=utils.network_to_bitcoinlib_format(self.get_network()))
        self.get_address()
        return self.wallet

    def get_default_sochain_url(self):
        """Get the default sochain url

        :returns: the default sochain url
        """
        return "https://sochain.com/api/v2"

    def set_sochain_url(self, url):
        """Set/Update the sochain url

        :param url: The new sochain url
        :type url: str
        """
        self.sochain_url = url

    def get_default_bitaps_url(self):
        """Get the default bitaps url

        :returns: the default bitaps url
        """
        return "https://api.bitaps.com"

    def set_bitaps_url(self, url):
        """Set/Update the bitaps url

        :param url: The new bitaps url
        :type url: str
        """
        self.bitaps_url = url

    def validate_address(self, network, address):
        """Validate the given address

        :param network: testnet or mainnet
        :type network: str
        :param address: address
        :type address: str
        :returns: True or False
        """
        return utils.validate_address(network, address)

    def get_address(self):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if self.phrase:
            self.address = self.wallet.get_key().address

            if not self.address:
                raise Exception('Address not defined')

            return self.address
        raise Exception('Phrase must be provided')

    def set_phrase(self, phrase: str):
        """Set/update a new phrase

        :param phrase: A new phrase
        :type phrase: str
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """
        if validate_phrase(phrase):
            self.phrase = phrase
            self.address = self.get_address()
            return self.address
        else:
            raise Exception("Invalid Phrase")

    def purge_client(self):
        """Purge client
        """
        self.phrase = ''