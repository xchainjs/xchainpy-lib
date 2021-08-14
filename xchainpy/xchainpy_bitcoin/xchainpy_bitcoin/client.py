import asyncio
from xchainpy_crypto.crypto import C, validate_phrase
from . import utils

from bitcoinlib.wallets import Wallet, wallet_delete_if_exists, wallet_delete
from bitcoinlib.services.services import Service
from xchainpy_client.models.tx_types import TX, TxHistoryParams, TxPage, TxParams
from . import crypto, sochain_api
from xchainpy_client.models.balance import Balance
from xchainpy_util.asset import Asset, AssetBTC





from xchainpy_client.utxo_client import UTXOClient
from xchainpy_util.chain import Chain
from . models.client_types import BitcoinClientParams

from bitcoinaddress import Wallet as BWallet


class IBitcoinClient():
    def derive_path(self):
        pass

    def get_fees_with_rates(self):
        pass

    def get_fees_with_memo(self):
        pass

    def get_fee_rates(self):
        pass


class Client(UTXOClient, IBitcoinClient):
    sochain_url = blockstream_url = ''

    # node_url = node_api_key = phrase = net = address = ''
    # wallet = None

    def __init__(self, params:BitcoinClientParams):
        """
        :param params: params
        :type params: BitcoinClientParams
        """
        UTXOClient.__init__(self, Chain.Bitcoin, params)
        # if self.phrase:
        #     self.__set_wallet(self.phrase)
        
        # phrase='atom green various power must another rent imitate gadget creek fat then'
        # wallet_delete_if_exists('Wallet', force=True)
        # self.wallet = Wallet.create(
        #     "Wallet", keys=self.phrase, witness_type='segwit', network='testnet')
        # hdkey = self.wallet.get_key().key()
        # p = hdkey.private_byte

        # a = crypto.mnemonic_to_private_key(mnemonic=phrase, derivation_path="m/44'/1'/0'/0/0")
        # a = a.Raw().ToBytes()



        self.set_sochain_url(params.sochain_url)
        self.set_blockstream_url(params.blockstream_url)

        # self.set_network(network)
        # self.set_phrase(phrase)

    def set_sochain_url(self, sochain_url:str):
        """Set/Update the sochain url

        :param sochain_url: The new sochain url
        :type sochain_url: str
        """
        self.sochain_url = sochain_url

    def set_blockstream_url(self, blockstream_url:str):
        """Set/Update the blockstream url

        :param blockstream_url: The new blockstream url
        :type blockstream_url: str
        """
        self.blockstream_url = blockstream_url

    # def set_network(self, network: str):
    #     """Set/update the current network

    #     :param network: "mainnet" or "testnet"
    #     :type network: str
    #     :returns: the client
    #     :raises: raises if network not provided
    #     :raises: `Invalid network' if the given network is invalid
    #     """
    #     UTXOClient.set_network(self, network)

    # def __set_wallet(self):
    #     """Set/update the current wallet

    #     :returns: the wallet
    #     """
    #     network = self.get_network()
    #     network = network if network == 'testnet' else 'bitcoin'

    #     # self.wallet = Wallet("Wallet")
    #     wallet_delete_if_exists('Wallet', force=True)
    #     self.wallet = Wallet.create(
    #         "Wallet", keys=self.phrase, witness_type='segwit', network=network)
    #     self.get_address()
    #     return self.wallet

    # def set_phrase(self, phrase:str, wallet_index:int=0):
    #     """Set/Update a new phrase

    #     :param phrase: A new phrase
    #     :type phrase: str
    #     :param wallet_index: HD wallet index
    #     :type wallet_index: int
    #     :returns: The address from the given phrase
    #     :raises: 'Invalid Phrase' if the given phrase is invalid
    #     """
    #     if not self.phrase or self.phrase != phrase:
    #         if not validate_phrase(phrase):
    #             raise Exception("invalid phrase")

    #         self.phrase = phrase
    #         self.__set_wallet(self.phrase)

    #     return self.get_address(wallet_index)


    def get_explorer_url(self) -> str:
        """Get explorer url
        :returns: the explorer url based on the network
        """
        return 'https://blockstream.info/testnet' if self.network == 'testnet' else 'https://blockstream.info'

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

    def get_address(self, index:int=0):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if index < 0:
            raise Exception('index must be greater than zero')
        
        if self.phrase:
            # self.address = self.wallet.get_key().address
            derivation_path = self.root_derivation_paths.testnet if self.get_network() == 'testnet' else self.root_derivation_paths.mainnet
            address = crypto.mnemonic_to_address(mnemonic=self.phrase, derivation_path=derivation_path + str(index), network=self.get_network())

            if not address:
                raise Exception('Address not defined')

            return address
        raise Exception('Phrase must be provided')

    # def get_network(self):
    #     """Get the current network
    #     :returns: the current network. (`mainnet` or `testnet`)
    #     """
    #     return self.net if self.net == 'testnet' else 'bitcoin'

    # def derive_path(self):
    #     return utils.get_derive_path().testnet if self.net == 'testnet' else utils.get_derive_path().mainnet

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
        """Get the BTC balance of a given address

        :param address: BTC address
        :type address: str
        :returns: The BTC balance of the address
        """
        balance = await utils.get_balance(self.sochain_url, address, self.get_network())
        return balance

    async def get_transactions(self, params:TxHistoryParams) -> TxPage:
        """Get transaction history of a given address with pagination options
        By default it will return the transaction history of the current wallet

        :param params: params
        :type params: TxHistoryParams
        :returns: The transaction history
        """
        try:
            transactions = await sochain_api.get_transactions(self.sochain_url, self.get_network(), self.get_address())
            total = transactions['total_txs']
            offset = params['offset'] if 'offset' in params else 0
            limit = params['limit'] if 'limit' in params else 10
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

        if you want to give a hash that is for mainnet and the current self.net is 'testnet',
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

    async def _calc_fee(self, fee_rate, memo):
        fee = await utils.calc_fee(fee_rate, memo)
        return fee

    # async def get_fees_with_rates(self, memo:str=''):
    #     """Get the rates and fees

    #     :param memo: The memo to be used for fee calculation (optional)
    #     :type memo: str
    #     :returns: The fees and rates
    #     """
    #     tx_fee = await sochain_api.get_suggested_tx_fee()

    #     rates = {
    #         'fastest': tx_fee * 5,
    #         'fast': tx_fee * 1,
    #         'average': tx_fee * 0.5
    #     }
    #     fees = {
    #         'fastest': utils.calc_fee(rates['fastest'], memo),
    #         'fast': utils.calc_fee(rates['fast'], memo),
    #         'average': utils.calc_fee(rates['average'], memo)
    #     }
    #     return {
    #         'rates': rates,
    #         'fees': fees
    #     }

    # async def get_fees(self):
    #     """Get the current fees

    #     :returns: The fees without memo
    #     """
    #     try:
    #         fees = (await self.get_fees_with_rates())['fees']
    #         return fees
    #     except Exception as err:
    #         raise Exception(str(err))

    # async def get_fees_with_memo(self, memo: str):
    #     """Get the fees for transactions with memo
    #     If you want to get `fees` and `fee_rates` at once, use `get_fees_with_rates` method

    #     :param memo: The memo to be used for fee calculation (optional)
    #     :type memo: str
    #     :returns: The fees with memo
    #     """
    #     try:
    #         fees = (await self.get_fees_with_rates(memo))['fees']
    #         return fees
    #     except Exception as err:
    #         raise Exception(str(err))

    # async def get_fee_rates(self):
    #     """Get the fee rates for transactions without a memo
    #     If you want to get `fees` and `fee_rates` at once, use `get_fees_with_rates` method

    #     :returns: The fee rate
    #     """
    #     try:
    #         rates = (await self.get_fees_with_rates())['rates']
    #         return rates
    #     except Exception as err:
    #         raise Exception(str(err))

    async def transfer(self, params:TxParams, fee_rate=None):
        """Transfer BTC

        :param amount: amount of BTC to transfer (don't multiply by 10**8)
        :type amount: int, float, decimal
        :param recipient: destination address
        :type recipient: str
        :param memo: optional memo for transaction
        :type memo: str
        :param fee_rate: fee rates for transaction
        :type fee_rate: int
        :returns: the transaction hash
        """
        if not fee_rate:
            fee_rates = await self.get_fee_rates()
            fee_rate = fee_rates.fast

        spend_pending_UTXO = False if params.memo else True

        t, utxos = await utils.build_tx(sochain_url=self.sochain_url, amount=int(params.amount*10**8), recipient=params.recipient,
                                        memo=params.memo, fee_rate=fee_rate, sender=self.get_address(), network=self.get_network(), 
                                        spend_pending_UTXO=spend_pending_UTXO)

        # derivation_path = self.root_derivation_paths.testnet if self.get_network() == 'testnet' else self.root_derivation_paths.mainnet
        # private_key = crypto.mnemonic_to_private_key(self.phrase, derivation_path, self.get_network())
        # private_bytes = private_key.Raw().ToBytes()
        # t.sign(private_bytes)

        network = self.network if self.network == 'testnet' else 'bitcoin'
        wallet_delete_if_exists('Wallet', force=True)
        wallet = Wallet.create(
            "Wallet", keys=self.phrase, witness_type='segwit', network=network)
        hdkey = wallet.get_key().key()
        t.sign(hdkey.private_byte)
        wallet_delete('Wallet', force=True)

        return await utils.broadcast_tx(self.blockstream_url, self.get_network(), t.raw_hex())


# xchainpy.xchainpy_bitcoin.xchainpy_bitcoin.client


import asyncio

async def main():
    c = Client(BitcoinClientParams(phrase='atom green various power must another rent imitate gadget creek fat then', network='testnet'))
    address = c.get_address()
    b = await c._get_suggested_fee_rate()
    f = 4

    params = TxParams(asset=AssetBTC, amount=0.0000001, recipient='tb1qymzatfxg22vg8adxlnxt3hkfmzl2rpuzpk8kcf', memo='testmemo')

    fee_rates = await c.get_fee_rates()
    fee_rate = fee_rates.fast


    tx_id = await c.transfer(params, fee_rate)
    a= 4

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(main())
finally:
    loop.run_until_complete(loop.shutdown_asyncgens())
    loop.close()
