from . models.client_types import LitecoinClientParams, LitecoinTxParams
from xchainpy_client.utxo_client import UTXOClient
from xchainpy_crypto.crypto import validate_phrase
from . import utils, crypto, sochain_api
from xchainpy_client.models.balance import Balance
from xchainpy_util.asset import Asset
from xchainpy_client.models import tx_types
from xchainpy_client.models.tx_types import TX, TxHistoryParams, TxPage
from xchainpy_client.utxo_client import UTXOClient
from xchainpy_util.chain import Chain



class Client(UTXOClient):

    def __init__(self, params:LitecoinClientParams):
        """
        :param params: params
        :type params: LitecoinClientParams
        """
        UTXOClient.__init__(self, Chain.Litecoin, params)

        self.set_sochain_url(params.sochain_url)

    def set_sochain_url(self, sochain_url:str):
        """Set/Update the sochain url

        :param sochain_url: The new sochain url
        :type sochain_url: str
        """
        self.sochain_url = sochain_url

    def get_explorer_url(self) -> str:
        """Get explorer url
        :returns: the explorer url based on the network
        """
        return 'https://tltc.bitaps.com' if self.network == 'testnet' else 'https://ltc.bitaps.com'

    def get_explorer_address_url(self, address:str) -> str:
        """Get the explorer url for the given address

        :param address: address
        :type address: str
        :returns: The explorer url for the given address based on the network
        """
        return f'{self.get_explorer_url()}/{address}'

    def get_explorer_tx_url(self, tx_id:str) -> str:
        """Get the explorer url for the given transaction id

        :param tx_id: tx_id
        :type tx_id: str
        :returns: The explorer url for the given transaction id based on the network
        """
        return f'{self.get_explorer_url()}/{tx_id}'

    def get_address(self, index:int=0):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if index < 0:
            raise Exception('index must be greater than zero')
        
        if self.phrase:
            derivation_path = self.root_derivation_paths.testnet if self.get_network() == 'testnet' else self.root_derivation_paths.mainnet
            address = crypto.mnemonic_to_address(mnemonic=self.phrase, derivation_path=derivation_path + str(index), network=self.get_network())

            if not address:
                raise Exception('Address not defined')

            return address
        raise Exception('Phrase must be provided')

    def validate_address(self, network, address):
        """Validate the given address

        :param network: testnet or mainnet
        :type network: str
        :param address: address
        :type address: str
        :returns: True or False
        """
        return utils.validate_address(network, address)

    async def get_balance(self, address):
        """Get the LTC balance of a given address

        :param address: LTC address
        :type address: str
        :returns: The LTC balance of the address
        """
        balance = await utils.get_balance(self.sochain_url, self.get_network(), address)
        return balance

    async def get_transactions(self, params:TxHistoryParams) -> TxPage:
        """Get transaction history of a given address with pagination options
        By default it will return the transaction history of the current wallet

        :param params: params
        :type params: TxHistoryParams
        :returns: The transaction history
        """
        try:
            transactions = await sochain_api.get_transactions(self.sochain_url, self.get_network(), params.address)
            total = transactions['total_txs']
            offset = params.offset or 0
            limit = params.limit or 10
            transactions['txs'] = transactions['txs'][offset:offset+limit]
            txs = []
            for tx in transactions['txs']:
                tx = await sochain_api.get_tx(self.sochain_url, self.get_network(), tx['txid'])
                tx = utils.parse_tx(tx)
                txs.append(tx)
 
            return TxPage(total=total, txs=txs)

        except Exception as err:
            raise Exception(str(err))

    async def get_transaction_data(self, tx_id:str) -> TX:
        """Get the transaction details of a given transaction id

        if you want to give a hash that is for mainnet and the current self.network is 'testnet',
        you should call self.set_network('mainnet') (and vice versa) and then call this method.

        :param tx_id: The transaction id
        :type tx_id: str
        :returns: The transaction details of the given transaction id
        """
        try:
            tx = await sochain_api.get_tx(self.sochain_url, self.get_network(), tx_id)
            tx = utils.parse_tx(tx)
            return tx
        except Exception as err:
            raise Exception(str(err))

    async def _get_suggested_fee_rate(self):
        fee_rate = await sochain_api.get_suggested_tx_fee()
        return fee_rate

    def _calc_fee(self, fee_rate, memo):
        fee = utils.calc_fee(fee_rate, memo)
        return fee

    async def transfer(self, params:LitecoinTxParams):
        """Transfer LTC

        :param params: transfer params
        :type params: LitecoinTxParams
        :returns: the transaction hash
        """
        if not params.fee_rate:
            fee_rates = await self.get_fee_rates()
            params.fee_rate = fee_rates.fast

        t, utxos = await utils.build_tx(sochain_url=self.sochain_url, amount=round(params.amount*10**8), recipient=params.recipient,
                                        memo=params.memo, fee_rate=params.fee_rate, sender=self.get_address(), network=self.get_network())

        derivation_path = self.root_derivation_paths.testnet if self.get_network() == 'testnet' else self.root_derivation_paths.mainnet
        derivation_path += str(params.wallet_index)
        private_key = crypto.mnemonic_to_private_key(self.phrase, derivation_path, self.get_network())
        private_bytes = private_key.Raw().ToBytes()
        t.sign(private_bytes)

        return await utils.broadcast_tx(self.sochain_url, self.get_network(), t.raw_hex())