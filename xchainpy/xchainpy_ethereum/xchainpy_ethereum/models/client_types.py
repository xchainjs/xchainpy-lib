from xchainpy_client.models.tx_types import TxParams
from xchainpy_client.models.types import Network, RootDerivationPaths, XChainClientParams
from xchainpy_util.asset import Asset


class EthereumClientParams(XChainClientParams):
    def __init__(self, wss_provider: str, etherscan_token: str, network: Network = Network.Testnet, phrase=None,
                 root_derivation_paths: RootDerivationPaths = RootDerivationPaths(
                     mainnet="m/44’/60’/0’/0",
                     # testnet path
                     testnet="m/44’/1’/0’/0"),):
        """
        Args:
            wss_provider: websocket provider, this is how web3 talks to blockchain
            etherscan_token: etherscan api token, to download non-erc20 token abi
            network: network, only testnet is supported as testnet
            phrase: phrase
            root_derivation_paths: root_derivation_paths
        """
        super().__init__(network, phrase, root_derivation_paths)
        self._wss_provider = wss_provider
        self._etherscan_token = etherscan_token

    @property
    def wss_provider(self):
        return self._wss_provider

    @wss_provider.setter
    def wss_provider(self, wss_provider):
        self._wss_provider = wss_provider

    @property
    def etherscan_token(self):
        return self._etherscan_token

    @etherscan_token.setter
    def etherscan_token(self, etherscan_token):
        self._etherscan_token = etherscan_token


