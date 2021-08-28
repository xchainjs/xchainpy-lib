from xchainpy_client.models.tx_types import TxParams
from xchainpy_client.models.types import Network, RootDerivationPaths, XChainClientParams
from xchainpy_util.asset import Asset, AssetBCH


class BitcoincashClientParams(XChainClientParams):

    def __init__(self, network:Network=Network.Testnet, phrase=None,
                 root_derivation_paths:RootDerivationPaths=RootDerivationPaths(
                     mainnet="m/44'/145'/0'/0/",
                     testnet="m/44'/1'/0'/0/"),
                 haskoin_url:str='https://api.haskoin.com'):
        """
        :param network: network
        :type network: str
        :param phrase: phrase 
        :type phrase: str
        :param root_derivation_paths: root_derivation_paths 
        :type root_derivation_paths: RootDerivationPaths
        :param haskoin_url: haskoinUrl 
        :type haskoin_url: str
        """
        super().__init__(network, phrase, root_derivation_paths)
        self._haskoin_url = haskoin_url

    @property
    def haskoin_url(self):
        return self._haskoin_url

    @haskoin_url.setter
    def haskoin_url(self, haskoin_url):
        self._haskoin_url = haskoin_url

    @property
    def blockstream_url(self):
        return self._blockstream_url

    @blockstream_url.setter
    def blockstream_url(self, blockstream_url):
        self._blockstream_url = blockstream_url


class BitcoincashTxParams(TxParams):
    def __init__(self, amount, recipient, memo='', fee_rate=None, wallet_index=0, asset:Asset=AssetBCH):
        """Transfer BCH

        :param amount: amount of BCH to transfer (don't multiply by 10**8)
        :type amount: int, float, decimal
        :param recipient: destination address
        :type recipient: str
        :param memo: optional memo for transaction
        :type memo: str
        :param fee_rate: fee rates for transaction
        :type fee_rate: int
        :param wallet_index: wallet_index
        :type wallet_index: int
        """
        TxParams.__init__(self, AssetBCH, amount, recipient, memo, wallet_index)
        self._fee_rate = fee_rate

    @property
    def fee_rate(self):
        return self._fee_rate

    @fee_rate.setter
    def fee_rate(self, fee_rate):
        self._fee_rate = fee_rate


