from . common import NodeAuth
from xchainpy_client.models.tx_types import TxParams
from xchainpy_client.models.types import Network, RootDerivationPaths, XChainClientParams
from xchainpy_util.asset import Asset, AssetLTC


class LitecoinClientParams(XChainClientParams):

    def __init__(self, network:Network=Network.Testnet, phrase=None,
                 root_derivation_paths:RootDerivationPaths=RootDerivationPaths(
                     # note this isn't bip44 compliant, but it keeps the wallets generated compatible to pre HD wallets
                     mainnet="m/84'/2'/0'/0/",
                     testnet="m/84'/1'/0'/0/"),
                 sochain_url:str='https://sochain.com/api/v2'):
        """
        :param network: network
        :type network: str
        :param phrase: phrase 
        :type phrase: str
        :param root_derivation_paths: root_derivation_paths 
        :type root_derivation_paths: RootDerivationPaths
        :param sochain_url: sochainUrl 
        :type sochain_url: str
        """
        super().__init__(network, phrase, root_derivation_paths)
        self._sochain_url = sochain_url

    @property
    def sochain_url(self):
        return self._sochain_url

    @sochain_url.setter
    def sochain_url(self, sochain_url):
        self._sochain_url = sochain_url


class LitecoinTxParams(TxParams):
    def __init__(self, amount, recipient, memo='', fee_rate=None, wallet_index=0, asset:Asset=AssetLTC):
        """Transfer LTC

        :param amount: amount of LTC to transfer (don't multiply by 10**8)
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
        TxParams.__init__(self, AssetLTC, amount, recipient, memo, wallet_index)
        self._fee_rate = fee_rate

    @property
    def fee_rate(self):
        return self._fee_rate

    @fee_rate.setter
    def fee_rate(self, fee_rate):
        self._fee_rate = fee_rate


