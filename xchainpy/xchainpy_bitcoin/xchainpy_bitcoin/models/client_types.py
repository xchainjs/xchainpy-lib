from xchainpy_client.models.types import Network, RootDerivationPaths, XChainClientParams


class BitcoinClientParams(XChainClientParams):

    def __init__(self, network:Network=Network.Testnet, phrase=None,
                 root_derivation_paths:RootDerivationPaths=RootDerivationPaths(
                     # note this isn't bip44 compliant, but it keeps the wallets generated compatible to pre HD wallets
                     mainnet="m/84'/0'/0'/0/",
                     testnet="m/84'/1'/0'/0/"),
                 sochain_url:str='https://sochain.com/api/v2', blockstream_url:str='https://blockstream.info'):
        """
        :param network: network
        :type network: str
        :param phrase: phrase 
        :type phrase: str
        :param root_derivation_paths: root_derivation_paths 
        :type root_derivation_paths: RootDerivationPaths
        :param sochain_url: sochainUrl 
        :type sochain_url: str
        :param blockstream_url: blockstreamUrl 
        :type blockstream_url: str
        """
        super().__init__(network, phrase, root_derivation_paths)
        self._sochain_url = sochain_url
        self._blockstream_url = blockstream_url

    @property
    def sochain_url(self):
        return self._sochain_url

    @sochain_url.setter
    def sochain_url(self, sochain_url):
        self._sochain_url = sochain_url

    @property
    def blockstream_url(self):
        return self._blockstream_url

    @blockstream_url.setter
    def blockstream_url(self, blockstream_url):
        self._blockstream_url = blockstream_url
