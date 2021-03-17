import asyncio
from binance_chain.http import AsyncHttpApiClient
from binance_chain.constants import KlineInterval
from binance_chain.environment import BinanceEnvironment
from binance_chain.messages import TransferMsg, Transfer, MultiTransferMsg
from binance_chain.wallet import Wallet
from typing import Optional
from datetime import datetime
import time

from xchainpy.xchainpy_client import interface
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy.xchainpy_binance import crypto
from xchainpy.xchainpy_binance import utils
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_binance.models.balance import BinanceBalance
from xchainpy.xchainpy_binance.models.coin import Coin
from binance_chain.constants import TransactionSide, TransactionType

class IBinanceClient():

    def purge_client(self):
        pass
    def get_bnb_client(self):
        pass
    def get_multi_send_fees(self): 
        pass
    def get_single_and_multi_fees(self): 
        pass
    def multi_send(self, coins, recipient, memo):
        pass

class Client(interface.IXChainClient, IBinanceClient):

    phrase = address = network = ''
    private_key = client = env = None

    def __init__(self, phrase, network='testnet'):
        """
        :param phrase: a phrase (mnemonic)
        :type phrase: str
        :param network: testnet or mainnet
        :type network: str
        """
        self.set_network(network)
        self.set_phrase(phrase)

    def get_client_url(self):
        """Get client url
        :returns: the client url for binance chain based on the network
        """
        return 'https://testnet-dex.binance.org' if self.network == 'testnet' else 'https://dex.binance.org'

    def get_bnb_client(self):
        return self.client

    def get_private_key(self):
        """Get private key

        :returns: the private key generated from the given phrase
        :raises: raise an exception if phrase not set
        """
        if not self.private_key:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.private_key = crypto.mnemonic_to_private_key(
                self.phrase)  # passPhrase ?
        return self.private_key

    def get_address(self):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if not self.address:
            self.address = crypto.private_key_to_address(
                self.get_private_key(), utils.get_prefix(self.network))
            if not self.address:
                raise Exception(
                    "Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key.")
        return self.address

    def set_phrase(self, phrase: str):
        """Set/Update a new phrase

        :param phrase: A new phrase
        :type phrase: str
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """

        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")

            self.phrase = phrase
            self.private_key = None
            self.address = ''

        return self.get_address()

    def set_network(self, network: str):
        """Set/update the current network

        :param network: "mainnet" or "testnet"
        :type network: str
        :returns: the client
        :raises: raises if network not provided
        :raises: `Invalid network' if the given network is invalid
        """
        if not network:
            raise Exception("Network must be provided")
        else:
            self.network = network
            # choose network (testnet or mainnet)
            if self.network == 'testnet':
                # initialise with Testnet environment
                self.env = BinanceEnvironment.get_testnet_env()
            elif self.network == 'mainnet':
                # initialise with mainnet environment
                self.env = BinanceEnvironment.get_production_env()
            else:
                raise Exception("Invalid network")

            self.client = AsyncHttpApiClient(env=self.env)
        self.address = ''
        return self.client

    def get_network(self):
        """Get the current network
        :returns: the current network. (`mainnet` or `testnet`)
        """
        return self.network

    async def get_balance(self, address: str = None, asset: Asset = None):
        """Get the balance of a given address

        :param address: By default, it will return the balance of the current wallet. (optional)
        :type If not set, it will return all assets available. (optional)
        :returns: The balance of the address
        """
        try:
            account = await self.client.get_account(address or self.get_address())
            binance_balances = account['balances']
            balances = []
            for balance in binance_balances:
                balance = BinanceBalance(balance)
                if not asset or str(balance.asset) == str(asset):
                    balances.append(balance)
            return balances

        except Exception as err:
            raise Exception(str(err))

    async def transfer(self, asset: Asset, amount, recipient, memo=''):
        """transfer balances

        :param asset: asset object containing : chain , symbol , ticker(optional)
        :type asset: Asset
        :param amount: amount of asset to transfer (don't multiply by 10**8)
        :type amount: int, float, decimal
        :param recipient: destination address
        :type recipient: str
        :param memo: optional memo for transaction
        :type memo: str
        :returns: the transaction hash
        :raises: raises if asset or amount or destination address not provided
        """
        wallet = Wallet(self.get_private_key(), env=self.env)

        if not asset:
            raise Exception('Asset must be provided')
        if not amount:
            raise Exception('Amount must be provided')
        if not recipient:
            raise Exception('Destination address must be provided')

        before_balance = await self.get_balance()
        before_balance_amount = before_balance[0].amount
        fee = await self.get_transfer_fee()
        fee = fee['fixed_fee_params']['fee'] * 10 ** -8
        if (amount + fee) > float(before_balance_amount):
            raise Exception(
                'input asset amout is higher than current (asset balance - transfer fee)')

        try:
            transfer_msg = TransferMsg(
                wallet=wallet,
                symbol=asset.symbol,
                amount=amount,
                to_address=recipient,
                memo=memo
            )
            transfer_result = await self.client.broadcast_msg(transfer_msg)
            return transfer_result[0]['hash']

        except Exception as err:
            raise Exception(str(err))

    async def multi_send(self, coins, recipient, memo=''):
        """Broadcast multi-send transaction 

        :param coins: contains assets and amounts
        :type coins: Array of Coin
        :param recipient: destination address
        :type recipient: str
        :param memo: optional memo for transaction
        :type memo: str
        :returns: the transaction hash
        :raises: raises if coins was not a list or destination address not provided
        """
        if not isinstance(coins, list):
            raise Exception('coins should be a list of Coin objects')

        wallet = Wallet(self.get_private_key(), env=self.env)

        transfers = [Transfer(symbol=coin.asset.symbol, amount=coin.amount) for coin in coins]

        try:
            multi_transfer_msg = MultiTransferMsg(
                wallet=wallet,
                transfers=transfers,
                to_address=recipient,
                memo=memo
            )
            transfer_result = await self.client.broadcast_msg(multi_transfer_msg)
            return transfer_result[0]['hash']

        except Exception as err:
            raise Exception(str(err))

    async def get_transfer_fee(self):
        """Get the current transfer fee

        :returns: The current transfer fee
        """
        try:
            fees = await self.client.get_fees()
            # the first fee from the fees that matches the condition, and returns None if no item matches
            transfer_fee = next(
                (fee for fee in fees if 'fixed_fee_params' in fee), None)
            return transfer_fee
        except Exception as err:
            raise Exception(str(err))

    async def get_fees(self):
        """Get the current fee

        :returns: The current fee 
        """
        try:
            transfer_fee = await self.get_transfer_fee()
            single_tx_fee = transfer_fee['fixed_fee_params']['fee'] * 10 ** -8
            return {
                'fast': single_tx_fee,
                'fastest': single_tx_fee,
                'average': single_tx_fee
            }
        except Exception as err:
            raise Exception(str(err))

    async def get_multi_send_fees(self):
        """Get the current fee for multi-send transaction

        :returns: The current fee for multi-send transaction
        """
        try:
            transfer_fee = await self.get_transfer_fee()
            multi_tx_fee = round(transfer_fee['multi_transfer_fee'] * 10 ** -8, 8)

            return {
                'fast': multi_tx_fee,
                'fastest': multi_tx_fee,
                'average': multi_tx_fee
            }
        except Exception as err:
            raise Exception(str(err))

    async def get_single_and_multi_fees(self):
        """Get the current fee for both single and multi-send transaction

        :returns: The current fee for both single and multi-send transaction
        """
        try:
            transfer_fee = await self.get_transfer_fee()
            multi_tx_fee = round(transfer_fee['multi_transfer_fee'] * 10 ** -8, 8)
            single_tx_fee = transfer_fee['fixed_fee_params']['fee'] * 10 ** -8

            return {
                'single': {
                    'fast': single_tx_fee,
                    'fastest': single_tx_fee,
                    'average': single_tx_fee
                },
                'multi': {
                    'fast': multi_tx_fee,
                    'fastest': multi_tx_fee,
                    'average': multi_tx_fee
                }
            }
        except Exception as err:
            raise Exception(str(err))

    def purge_client(self):
        """Purge client
        """
        self.phrase = ''
        self.address = ''
        self.private_key = None
        self.client.session.close()

    def validate_address(self, address: str, prefix: str):
        """Validate the given address

        :param address: address
        :type address: str
        :param prefix: bnb or tbnb
        :type prefix: str
        :returns: True or False
        """
        return True if crypto.check_address(address, prefix) else False

    async def search_transactions(self, params: dict = None):
        """Search transactions with parameters

        :param params: a dict that could be empty or have these fields:
            address (default = self.address)
            symbol
            side (SEND or RECEIVE)
            tx_asset
            tx_type
            height
            offset (default = 0)
            limit (default = 500)
            start_time (default = 90 days ago)
            end_time: (default = now)
            
            see the link below for further information:
            https://docs.binance.org/api-reference/dex-api/paths.html#apiv1transactions

        :type params: dict
        :returns: The parameters to be used for transaction search
        """

        params['address'] = params['address'] or self.address

        network_changed = False
        if params['address'].startswith('bnb') and self.get_network() == 'testnet':
            network_changed = True
            self.set_network('mainnet')
        elif params['address'].startswith('tbnb') and self.get_network() == 'mainnet':
            network_changed = True
            self.set_network('testnet')

        now = datetime.now()
        now = time.mktime(now.timetuple()) * 1000
        now = int(now)

        diff_time = 90 * 24 * 60 * 60 * 1000
        end_time = now
        start_time = end_time - diff_time

        if 'start_time' in params and not 'end_time' in params:
            params['end_time'] = int(params['start_time']) + diff_time
        elif 'end_time' in params and not 'start_time' in params:
            params['start_time'] = int(params['end_time']) - diff_time
        elif not 'start_time' in params and not 'end_time' in params:
            params['start_time'] = start_time
            params['end_time'] = end_time
        
        try:
            transactions = await self.client.get_transactions(**params)

            if network_changed:
                self.set_network('testnet' if self.network == 'mainnet' else 'mainnet')

            txs = list(map(utils.parse_tx, transactions['tx']))

            return {
                'total': transactions['total'],
                'tx': txs
            }

        except Exception as err:
            raise Exception(str(err))

    async def get_transactions(self, params: tx_types.TxHistoryParams):
        """Get transaction history of a given address with pagination options
        By default it will return the transaction history of the current wallet

        :param params: params
        :type params: tx_types.TxHistoryParams
        :returns: The parameters to be used for transaction search
        """

        transaction_params = {}
        transaction_params['address'] = params.address
        transaction_params['tx_asset'] = params.asset.symbol if params.asset else None
        transaction_params['limit'] = params.limit
        transaction_params['offset'] = params.offset
        if params.start_time:
            transaction_params['start_time'] = params.start_time

        try:
            transactions = await self.search_transactions(transaction_params)
            return transactions
        except Exception as err:
            raise Exception(str(err))

    async def get_transaction_data(self, tx_id):
        """Get the transaction details of a given transaction id

        if you want to give a hash that is for mainnet and the current self.network is 'testnet',
        you should call self.set_network('mainnet') (and vice versa) and then call this method.

        :param tx_id: The transaction id
        :type tx_id: str
        :returns: The parameters to be used for transaction search
        """

        try:
            address = ''
            transaction = await self.client.get_transaction(tx_id)
            msgs = transaction['tx']['value']['msg']
            if len(msgs):
                msg = msgs[0]['value']
                if msg['inputs'] and len(msg['inputs']):
                    address = msg['inputs'][0]['address']
                elif msg['outputs'] and len(msg['outputs']):
                    address = msg['outputs'][0]['address']

            transactions = await self.search_transactions({'address': address})
            transaction = next(filter(lambda v: v.tx_hash == tx_id , transactions['tx']), None)
            if transaction:
                return transaction

            raise Exception('transaction not found')
        except Exception as err:
            raise Exception(str(err))