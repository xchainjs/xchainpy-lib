from xchainpy.xchainpy_bitcoincash.xchainpy_bitcoincash.models.api_types import Transaction
from xchainpy_client.models.tx_types import TX, TxHistoryParams, TxPage
from xchainpy_client.utxo_client import UTXOClient
from xchainpy_util.chain import Chain
from . import utils, crypto, haskoin_api
from . models.client_types import BitcoincashClientParams, BitcoincashTxParams
from bitcash import transaction, PrivateKey, PrivateKeyTestnet, network


class Client(UTXOClient):
    def __init__(self, params:BitcoincashClientParams):
        """
        :param params: params
        :type params: BitcoincashClientParams
        """
        UTXOClient.__init__(self, Chain.BitcoinCash, params)
        self.set_haskoin_url(params.haskoin_url)

    def set_haskoin_url(self, haskoin_url:str):
        """Set/Update the haskoin url

        :param haskoin_url: The new haskoin url
        :type haskoin_url: str
        """
        self.haskoin_url = haskoin_url
    
    def get_explorer_url(self) -> str:
        """Get explorer url
        :returns: the explorer url based on the network
        """
        return 'https://www.blockchain.com/bch-testnet' if self.network == 'testnet' else 'https://www.blockchain.com/bch'

    def get_explorer_address_url(self, address:str) -> str:
        """Get the explorer url for the given address

        :param address: address
        :type address: str
        :returns: The explorer url for the given address based on the network
        """
        return f'{self.get_explorer_url()}/address/{address}'

    def get_explorer_tx_url(self, tx_id:str) -> str:
        """Get the explorer url for the given transaction id

        :param tx_id: tx_id
        :type tx_id: str
        :returns: The explorer url for the given transaction id based on the network
        """
        return f'{self.get_explorer_url()}/tx/{tx_id}'


    def __get_private_key(self, index:int=0):
        """Get private key

        :param phrase: The phrase to be used for generating privkey
        :type phrase: str
        :returns: The privkey generated from the given phrase
        """
        try:
            derivation_path = self.root_derivation_paths.testnet if self.get_network() == 'testnet' else self.root_derivation_paths.mainnet
            derivation_path += str(index)
            privKey = crypto.mnemonic_to_private_key(self.phrase, derivation_path, self.network)
            return privKey
        except:
            raise Exception("Invalid Phrase")


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

    def validate_address(self, address):
        """Validate the given address

        :param network: testnet or mainnet
        :type network: str
        :param address: address
        :type address: str
        :returns: True or False
        """
        return utils.validate_address(address)

    async def get_balance(self, address):
        """Get the BCH balance of a given address

        :param address: BCH address
        :type address: str
        :returns: The BCH balance of the address
        """
        balance = await utils.get_balance(self.haskoin_url, self.get_network(), address)
        return balance

    async def get_transactions(self, params:TxHistoryParams) -> TxPage:
        """Get transaction history of a given address with pagination options
        By default it will return the transaction history of the current wallet

        :param params: params
        :type params: TxHistoryParams
        :returns: The transaction history
        """
        try:
            account = await haskoin_api.get_account(self.haskoin_url, self.get_network(), params.address)
            if not account:
                    raise Exception("Invalid Address")

            offset = params.offset or 0
            limit = params.limit or 10
            transactions = await haskoin_api.get_transactions(self.haskoin_url, self.get_network(), params.address, offset, limit)
            if not transactions:
                    raise Exception("Transactions could not found for this address")

            total = account.txs
            txs = []
            for tx in transactions:
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
            tx = await haskoin_api.get_transaction(self.haskoin_url, self.get_network(), tx_id)
            if not tx:
                raise Exception("Invalid tx_id")
            tx = utils.parse_tx(tx)
            return tx
        except Exception as err:
            raise Exception(str(err))

    async def _get_suggested_fee_rate(self):
        fee_rate = await haskoin_api.get_suggested_tx_fee()
        return fee_rate

    def _calc_fee(self, fee_rate, memo):
        fee = utils.calc_fee(fee_rate, memo)
        return fee

    async def transfer(self, params:BitcoincashTxParams):
        """Transfer BCH

        :param params: transfer params
        :type params: BitcoincashTxParams
        :returns: the transaction hash
        """
        try:
            if not params.fee_rate:
                fee_rates = await self.get_fee_rates()
                params.fee_rate = fee_rates.fast

            KeyClass = PrivateKeyTestnet if self.get_network() == "testnet" else PrivateKey
            key = KeyClass.from_hex(self.__get_private_key(params.wallet_index).Raw().ToHex())

            tx_hex = await utils.build_tx(self.haskoin_url, params.amount , params.recipient , params.memo , params.fee_rate , self.get_address(),self.get_network(), key)
            
            network.NetworkAPI.broadcast_tx_testnet(tx_hex)
            return transaction.calc_txid(tx_hex)
            
        except Exception as err:
            raise Exception(str(err))