
import asyncio
from xchainpy.xchainpy_crypto.crypto import validate_phrase
from xchainpy.xchainpy_client.interface import IXChainClient
from xchainpy.xchainpy_bitcoin import utils

from bitcoinlib.wallets import Wallet
from bitcoinlib.wallets import *
from xchainpy.xchainpy_client.models import tx_types
from xchainpy.xchainpy_bitcoin import sochain_api
from xchainpy.xchainpy_client.models.balance import Balance
from xchainpy.xchainpy_util.asset import Asset


class IBitcoinClient():
    def derive_path(self):
        pass

    def get_fees_with_rates(self):
        pass

    def get_fees_with_memo(self):
        pass

    def get_fee_rates(self):
        pass


class Client(IBitcoinClient, IXChainClient):

    node_url = node_api_key = phrase = net = address = ''
    wallet = None

    def __init__(self, phrase, network='testnet'):
        """
        :param phrase: a phrase (mnemonic)
        :type phrase: str
        :param network: testnet or mainnet
        :type network: str
        """
        self.set_network(network)
        self.set_phrase(phrase)
        self.service = Service(network=self.get_network())

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
            if not network in ['testnet', 'mainnet']:
                raise Exception('Invalid network')
            else:
                self.net = network

    def set_wallet(self, phrase):
        """Set/update the current wallet

        :param phrase: A new phrase
        :type phrase: str
        :returns: the wallet
        """
        # self.wallet = Wallet("Wallet")
        wallet_delete_if_exists('Wallet', force=True)
        self.wallet = Wallet.create(
            "Wallet", keys=self.phrase, witness_type='segwit', network=self.get_network())
        return self.wallet

    def set_phrase(self, phrase: str):
        """Set/Update a new phrase

        :param phrase: A new phrase
        :type phrase: str
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """
        if validate_phrase(phrase):
            self.phrase = phrase
            self.set_wallet(self.phrase)
            address = self.get_address()
            return address
        else:
            raise Exception("Invalid Phrase")

    def purge_client(self):
        """Purge client
        """
        self.phrase = ''

    def get_network(self):
        """Get the current network
        :returns: the current network. (`mainnet` or `testnet`)
        """
        return self.net if self.net == 'testnet' else 'bitcoin'

    def derive_path(self):
        return utils.get_derive_path().testnet if self.net == 'testnet' else utils.get_derive_path().mainnet

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

    async def get_balance(self, address: str = None):
        """Get the BTC balance of a given address

        :param address: By default, it will return the balance of the current wallet. (optional)
        :type address: str
        :returns: The BTC balance of the address.
        """
        try:
            amount = await sochain_api.get_balance(self.net, address or self.address)
            balance = Balance(Asset.from_str('BTC.BTC'), amount)
            return balance
        except Exception as err:
            raise Exception(str(err))

    async def get_transactions(self, params: tx_types.TxHistoryParams):
        """Get transaction history of a given address with pagination options
        By default it will return the transaction history of the current wallet

        :param params: params
        :type params: tx_types.TxHistoryParams
        :returns: The transaction history
        """
        try:
            transactions = await sochain_api.get_transactions(self.net, self.address)
            total = transactions['total_txs']
            txs = []
            for tx in transactions['txs']:
                tx = await sochain_api.get_tx(self.net, tx['txid'])
                tx = utils.parse_tx(tx)
                txs.append(tx)

            return {
                'total': total,
                'tx': txs
            }
        except Exception as err:
            raise Exception(str(err))

    async def get_transaction_data(self, tx_id: str):
        """Get the transaction details of a given transaction id

        if you want to give a hash that is for mainnet and the current self.net is 'testnet',
        you should call self.set_network('mainnet') (and vice versa) and then call this method.

        :param tx_id: The transaction id
        :type tx_id: str
        :returns: The transaction details of the given transaction id
        """
        try:
            tx = await sochain_api.get_tx(self.net, tx_id)
            tx = utils.parse_tx(tx)
            return tx
        except Exception as err:
            raise Exception(str(err))

    async def get_fees_with_rates(self, memo: str = ''):
        """Get the rates and fees

        :param memo: The memo to be used for fee calculation (optional)
        :type memo: str
        :returns: The fees and rates
        """
        tx_fee = await sochain_api.get_suggested_tx_fee()

        rates = {
                'fast': tx_fee * 5,
                'fastest': tx_fee * 1,
                'average': tx_fee * 0.5
            }
        fees = {
                'fast': utils.calc_fee(rates['fast'], memo),
                'fastest': utils.calc_fee(rates['fastest'], memo),
                'average': utils.calc_fee(rates['average'], memo),
            }
        return {
            rates,
            fees
        }

    async def get_fees(self):
        """Get the current fees

        :returns: The fees without memo
        """
        try:
            fees = (await self.get_fees_with_rates())['fees']
            return fees
        except Exception as err:
            raise Exception(str(err))

    async def get_fees_with_memo(self, memo: str):
        """Get the fees for transactions with memo
        If you want to get `fees` and `fee_rates` at once, use `get_fees_with_rates` method

        :param memo: The memo to be used for fee calculation (optional)
        :type memo: str
        :returns: The fees with memo
        """
        try:
            fees = (await self.get_fees_with_rates(memo))['fees']
            return fees
        except Exception as err:
            raise Exception(str(err))

    async def get_fee_rates(self):
        """Get the fee rates for transactions without a memo
        If you want to get `fees` and `fee_rates` at once, use `get_fees_with_rates` method

        :returns: The fee rate
        """
        try:
            rates = (await self.get_fees_with_rates())['rates']
            return rates
        except Exception as err:
            raise Exception(str(err))


    def validate_address(self, network, address):
        """Validate the given address

        :param network: testnet or mainnet
        :type network: str
        :param address: address
        :type address: str
        :returns: True or False
        """
        return utils.validate_address(network, address)


    async def transfer(self, amount, recipient, memo:str=None, fee_rate=None):
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
        
        t, utxos = await utils.build_tx(amount=int(amount*10**8), recipient=recipient, memo=memo, fee_rate=fee_rate,
                                        sender=self.get_address(), network=self.net)

        hdkey = self.wallet.get_key().key()
        t.sign(hdkey.private_byte)

        return await utils.broadcast_tx(self.net, t.raw_hex())