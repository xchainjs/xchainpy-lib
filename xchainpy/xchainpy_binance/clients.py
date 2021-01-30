from binance_chain.http import AsyncHttpApiClient
from binance_chain.constants import KlineInterval
from binance_chain.environment import BinanceEnvironment
from binance_chain.messages import TransferMsg
from binance_chain.wallet import Wallet

from xchainpy.xchainpy_client import interface
from xchainpy.xchainpy_crypto import crypto as xchainpy_crypto
from xchainpy.xchainpy_binance import crypto
from xchainpy.xchainpy_binance import utils
from xchainpy.xchainpy_util.asset import Asset
from xchainpy.xchainpy_binance.balance import BinanceBalance

class Client(interface.IXChainClient): # create an interface for binance methods (getprivate_key, get_client_url and ...)

    phrase = address = network = ''
    private_key = client = env = None
    
    def __init__(self, phrase, network = 'testnet'):
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

    def get_private_key(self):
        """Get private key

        :returns: the private key generated from the given phrase
        :raises: raise an exception if phrase not set
        """
        if not self.private_key:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.private_key = crypto.mnemonic_to_private_key(self.phrase) # passPhrase ?
        return self.private_key

    def get_address(self):
        """Get the current address

        :returns: the current address
        :raises: Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        if not self.address:
            self.address = crypto.private_key_to_address(self.get_private_key(), utils.get_prefix(self.network))
            if not self.address :
                raise Exception("Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key.")
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
            print(str(err))
        

    async def transfer(self, asset : Asset , amount , recipient , memo=''):
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
            print(err)

    def get_fees(self):
        pass

# async def main():

#     asset = Asset('BNB', 'BNB')
#     recipient = 'tbnb185tqzq3j6y7yep85lncaz9qeectjxqe5054cgn'
#     amount = 0.001

#     phrase = 'legend civil salute surface insect since gap unfold bleak endless near push damp rate foster hand nature rib repeat novel cross pizza squirrel topple'
#     a = Client(phrase, 'testnet')

#     b = await a.get_balance()
#     o = b[0]['amount']
#     g = b[0]['asset']
#     g = g['ticker']

#     y = a.private_key
#     return 4

# import asyncio

# loop = asyncio.get_event_loop()
# try:
#     loop.run_until_complete(main())
# finally:
#     loop.run_until_complete(loop.shutdown_asyncgens())
#     loop.close()