from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_client.models.balance import Balance
from xchainpy.xchainpy_bitcoincash import haskoin_api
from bitcash.wallet import Key, PrivateKeyTestnet
from cashaddress import convert
from cashaddress.convert import Address
from xchainpy.xchainpy_bitcoincash.crypto import mnemonic_to_private_key, private_key_to_address
from mnemonic.mnemonic import Mnemonic
from xchainpy.xchainpy_crypto.crypto import validate_phrase
from xchainpy.xchainpy_bitcoincash import utils
from xchainpy.xchainpy_client.interface import IXChainClient
from bitcash import transaction, PrivateKey, PrivateKeyTestnet, network

class IBitcoinCashClient():
    def derive_path(self) -> str :
        pass
    def get_fees_with_rates(self , memo = None):
        pass
    def get_fees_with_memo(self):
        pass
    def get_fee_rates(self):
        pass

class Client(IBitcoinCashClient , IXChainClient):
    def __init__(self, phrase:str, network='testnet', client_url:utils.ClientUrl=None):
        self.set_network(network)
        self.client_url = client_url if client_url else self.get_default_client_url()
        self.set_phrase(phrase)

    def get_default_client_url(self) -> utils.ClientUrl:
        """Get default ClientURL based on the network

        :returns: the transaction hash
        """
        return utils.ClientUrl("https://api.haskoin.com/bchtest" ,"https://api.haskoin.com/bch")

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

    def get_address(self):
        """Get the current address

        :returns: The current address
        :raises: "Phrase must be provided" if phrase has not been set before
        :raises: "Address not defined" if failed creating account from phrase
        """
        if self.phrase:
            try:
                priv_key = self.get_private_key(self.phrase)
                address = private_key_to_address(priv_key, self.network)
                return str(address)
            except:
                raise Exception("Address not defined")
        else:
            raise Exception("Phrase must be provided")

    def get_private_key(self , phrase:str=None):
        """Get private key

        :param phrase: The phrase to be used for generating privkey
        :type phrase: str
        :returns: The privkey generated from the given phrase
        """
        try:
            privKey = mnemonic_to_private_key(phrase or self.phrase, self.network)
            return privKey
        except:
            raise Exception("Invalid Phrase")


    def derive_path(self):
        """Get DerivePath

        :returns: The bitcoin cash derivation path based on the network
        """
        return utils.get_derive_path().testnet if self.network == 'testnet' else utils.get_derive_path().mainnet

    def purge_client(self):
        """Purge client
        """
        self.phrase = ''

    def get_network(self):
        """Get the current network

        :returns: The current network. (mainnet or testnet)
        """
        return self.network

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
            self.network = network

    def set_client_url(self , url : utils.ClientUrl):
        """Set/Update the node url

        :param url: The new node url
        :type url: str
        """
        self.client_url = url

    def get_client_url(self):
        """Get the client url

        :returns: The client url based on the current network
        """
        return self.get_client_url_by_network(self.get_network())

    def get_client_url_by_network(self, network):
        """Get the client url by network

        :param network: testnet or mainnet
        :type network: str
        :returns: The client url based on the network
        """
        if network == "testnet":
            return self.client_url.testnet
        if network == "mainnet":
            return self.client_url.mainnet
        raise Exception('invalid network')

    def validate_address(self, address: str):
        """Validate the given address

        :param address: address
        :type address: str
        :returns: true or false
        """
        return convert.is_valid(address)

    async def get_balance(self, address:str=""):
        """Get the BCH balance of a given address

        :param address: By default, it will return the balance of the current wallet. (optional)
        :type address: str
        :returns: The BCH balance of the address
        :raises: "Invalid address" if the given address is an invalid address
        """
        try:            
            account = await haskoin_api.get_account(self.get_client_url() , address or self.get_address())
            if not account:
                raise Exception("Invalid Address")
            
            balance = Balance(Asset.from_str("BCH.BCH"), account.confirmed * 10 ** -8)
            return balance
                
        except Exception as err:
            raise Exception(str(err))

    async def get_transaction_data(self, tx_id: str):
        """Get the transaction details of a given transaction id

        :param tx_id: The transaction id
        :type str: str
        :returns: The transaction details of the given transaction id
        :raises: "Invalid address" if the given transaction id is an invalid one
        """
        try:
            tx = await haskoin_api.get_transaction(self.get_client_url() , tx_id)

            if not tx:
                raise Exception("Invalid tx_id")

            data = utils.parse_tx(tx)
            return data

        except Exception as err:
            raise Exception(str(err))

    async def get_fees_with_rates(self, memo: str = ''):
        """Get the rates and fees

        :param memo: The memo to be used for fee calculation (optional)
        :type memo: str
        :returns: The fees and rates
        """
        next_block_fee_rates = await haskoin_api.get_suggested_tx_fee()

        rates = {
            'fastest': next_block_fee_rates * 5,
            'fast': next_block_fee_rates * 1,
            'average': next_block_fee_rates * 0.5
        }
        fees = {
            'fastest': utils.calc_fee(rates['fastest'], memo),
            'fast': utils.calc_fee(rates['fast'], memo),
            'average': utils.calc_fee(rates['average'], memo)
        }
        return {
            'rates': rates,
            'fees': fees
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
    

    async def transfer(self, amount, recipient, memo: str = None, fee_rate=None) -> str:
        """Transfer BCH

        :param amount: amount of BTC to transfer (don't multiply by 10**8)
        :type amount: int, float, decimal
        :param recipient: destination address
        :type recipient: str
        :param memo: optional memo for transaction
        :type memo: str
        :param fee_rate: fee rates for transaction
        :type fee_rate: int
        :returns: The transaction hash
        """
        try:
            fee_rate = fee_rate or (await self.get_fee_rates())['fast']

            KeyClass = PrivateKeyTestnet if self.get_network() == "testnet" else PrivateKey
            key = KeyClass.from_hex(self.get_private_key())

            tx_hex = await utils.build_tx(amount , recipient , memo , fee_rate , self.get_address(),self.get_network(), self.get_client_url(), key)
            
            network.NetworkAPI.broadcast_tx_testnet(tx_hex)
            return transaction.calc_txid(tx_hex)
            

        except Exception as err:
            raise Exception(str(err))