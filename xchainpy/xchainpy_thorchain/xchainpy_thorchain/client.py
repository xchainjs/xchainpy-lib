import binascii
from xchainpy.xchainpy_client.xchainpy_client.models.types import Network, RootDerivationPaths
from xchainpy.xchainpy_thorchain.xchainpy_thorchain.cosmos.models.StdTxFee import StdTxFee
from .cosmos.models.StdTx import StdTx
import http3
import json
from xchainpy_client import interface
from xchainpy_crypto import crypto as xchainpy_crypto
from . import utils
from . import crypto
from .cosmos.models.MsgCoin import MsgCoin
from .cosmos.models.MsgNativeTx import MsgNativeTx
from .cosmos.sdk_client import CosmosSDKClient
from .cosmos import message
from .utils import DEFAULT_GAS_VALUE, DEPOSIT_GAS_VALUE, asset_to_string, frombech32, get_chain_id, get_default_explorer_urls, getDenomWithChain, get_asset


class IThorchainClient():
    def set_client_url(self, client_url):
        pass

    def set_explorer_url(self):
        pass

    def get_explorer_node_url(self):
        pass

    def deposit(self):
        pass


class Client(interface.IXChainClient, IThorchainClient):

    derive_path = "m/44'/118'/0'/0/0"
    phrase = address = network = ''
    private_key = None

    def __init__(self, phrase: str ,chain_ids ,root_derivation_path : RootDerivationPaths = RootDerivationPaths("44'/931'/0'/0/" ,"44'/931'/0'/0/" , "44'/931'/0'/0/"), network: str = "testnet", client_url: str = None, explorer_urls: str = None) -> None:
        """Constructor

        Client has to be initialised with network type and phrase.
        It will throw an error if an invalid phrase has been passed.

        :param phrase: phrase of wallet (mnemonic) will be set to the Class
        :param network: network of chain can either be `testnet` or `mainnet`
        :param client_url: client url can be added manually
        :param explorer_url: explorer url can be added manually
        :type phrase: string
        :type network: string
        :type client_url: string
        :type explorer_url: string
        :return: returns void (None)
        :rtype: None
        """
        self.root_derivation_path = root_derivation_path
        self.network = network
        self.client_url = client_url or self.get_default_client_url()
        self.explorer_url = explorer_urls or get_default_explorer_urls()
        self.chain_ids = chain_ids
        self.cosmos_client = CosmosSDKClient(server=self.client_url[self.network]['node'],prefix=self.get_prefix(self.network),chain_id=self.get_chain_id(self.network))

        if phrase:
            self.set_phrase(phrase)

    async def purge_client(self) -> None:
        """Purge client

        :return: returns void (None)
        :rtype: None
        """
        self.phrase = self.address = ''
        self.private_key = None
        await self.cosmos_client.client.close()

    def set_network(self, network: str) -> None:
        """Set/update the current network.

        :param netowrk: network `mainnet` or `testnet`
        :type network: string
        :returns: Nothing (Void/None)
        :raises:
            Exception: "Network must be provided". -> Thrown if network has not been set before.
        """
        if not network:
            raise Exception('Network must be provided')
        else:
            self.network = network
            self.address = ''

    def set_phrase(self, phrase: str) -> str:
        if not self.phrase or self.phrase != phrase:
            if not xchainpy_crypto.validate_phrase(phrase):
                raise Exception("invalid phrase")

            self.phrase = phrase
            self.private_key = None
            self.address = ''

        return self.get_address()

    def get_network(self) -> str:
        """Get the current network.

        :returns: The current network. (`mainnet` or `testnet`)
        :rtype: string
        """
        return self.network

    def set_client_url(self, client_url: str) -> None:
        """Set/update the client URL.

        :param client_url: The client url to be set.
        :type client_url: string
        :returns: Nothing (None)
        :rtype: None
        """
        self.client_url = client_url

    def validate_address(self, address: str, prefix: str):
        """Validate the given address

        :param address: address
        :type address: str
        :param prefix: bnb or tbnb
        :type prefix: str
        :returns: True or False
        """
        return True if crypto.check_address(address, prefix) else False

    def get_default_client_url(self) -> object:
        """Get the client url.

        :returns: The client url (both node, rpc) for thorchain based on the network.
        :rtype: {NodeUrl} as a object
        """
        return {
            "testnet": {
                "node": 'https://testnet.thornode.thorchain.info',
                "rpc": 'https://testnet.rpc.thorchain.info',
            },
            "mainnet": {
                "node": 'https://thornode.ninerealms.com',
                "rpc": 'https://rpc.thorchain.info',
            },
            "stagenet":{
                "node": "https://stagenet-thornode.ninerealms.com",
                "rpc":"https://stagenet-rpc.ninerealms.com"
            }
        }



    def get_explorer_tx_url(self , tx_id: str) -> str:
        """Get the explorer url for the given transaction id.
   
        :param tx_id: network
        :type tx_id: string
        :returns: The explorer url for the given transaction id.
        :rtype: string
        """
        return f'{self.get_default_explorer_url()}/txs/${tx_id}'

    def get_prefix(self, network) -> str:
        """Get address prefix based on the network.

        :param network: network
        :type network: string
        :returns: The address prefix based on the network.
        :rtype: string
        """
        if network == "mainnet":
            return "thor"
        elif network == "stagenet":
            return "sthor"
        elif network == "testnet":
            return "tthor"

    def get_chain_id(self , network) -> str:
        """Get the chain id.

        :returns: The chain id based on the network.
        :rtype: string
        """
        return self.chain_ids[network if network != None else self.network]

    def get_private_key(self , wallet_index = 0) -> bytes:
        """Get private key.

        :returns: The private key generated from the given phrase
        :rtype: bytes
        :raises: 
            Exception: {"Phrase not set"} -> Throws an error if phrase has not been set before
        """



        if not self.private_key:
            if not self.phrase:
                raise Exception('Phrase not set')

            self.private_key = self.cosmos_client.get_priv_key_from_mnemonic(self.phrase , self.get_full_derivation_path(wallet_index))

        return self.private_key

    def get_full_derivation_path(self , index : int) -> str:
        if self.network == "testnet":
            return f'{self.root_derivation_path.testnet}{index}'
        elif self.network == "mainnet":
            return f'{self.root_derivation_path.mainnet}{index}'
        elif self.network == "stagenet":
            return f'{self.root_derivation_path.stagenet}{index}'
        

    def get_address(self , index = 0) -> str:
        """Get the current address

        :returns: the current address
        :rtype: string
        :raises: 
            Exception: {"Address has to be set. Or set a phrase by calling `setPhrase` before to use an address of an imported key."}
                        -> Raises if phrase has not been set before. A phrase is needed to create a wallet and to derive an address from it.
        """
        address = self.cosmos_client.get_address_from_mnemonic(self.phrase, self.get_full_derivation_path(index))
        if not address:
            raise Exception("address not defined")
        
        return address

    async def get_balance(self, address: str = None, assets = None) -> list:
        """
         Get the balance of a given address.

         :param address: address By default, it will return the balance of the current wallet. (optional)
         :param asset: asset If not set, it will return all assets available. (optional)
         :returns: The balance of the address.
         :rtype: list
        """
        if not address:
            address = self.get_address()
        response = await self.cosmos_client.get_balance(address)
        response = response["result"]

        balances = []
        for balance in response:
            asset = None
            if balance['denom']:
                asset = get_asset(balance['denom'])
            else:
                asset = {"chain" : "THOR", "symbol": "RUNE" , "ticker" : "RUNE"}
            amount = balance['amount']
            balances.append({"asset" : asset,"amount" : amount})
        if assets:
            return list(filter(lambda x : any(asset_to_string(x["asset"]) == asset_to_string(element) for element in assets) , balances))
        return balances

    async def get_transaction_data(self, tx_id: str) -> object:
        """Get the transaction details of a given transaction id

        if you want to give a hash that is for mainnet and the current self.net is 'testnet',
        you should call self.set_network('mainnet') (and vice versa) and then call this method.

        :param tx_id: The transaction id
        :type tx_id: str
        :returns: The transaction details of the given transaction id
        :rtype: object
        """
        try:
            tx_result = await self.cosmos_client.txs_hash_get(tx_id)
            if not tx_result:
                raise Exception("transaction not found")
            return tx_result
        except Exception as err:
            raise Exception(err)

    async def transfer(self, amount: int, recipient: str, asset = {"symbol": "rune"}, memo: str = "") -> dict:
        """Transfer balances with MsgSend

        :param amount: amount which you want to send
        :param recipient: the address of recipient to be send
        :param asset: asset need to be send
        :param memo: memo of the transaction
        :type amount: int
        :type recipient: string
        :type asset: string
        :type memo: string
        :returns: The transaction hash
        :rtype: object
        """
        if not asset:
            raise Exception('Asset must be provided')
        if not amount:
            raise Exception('Amount must be provided')
        if not recipient:
            raise Exception('Destination address must be provided')

        before_balance = await self.get_balance()
        if len(before_balance) == 0:
            raise Exception('No balance in this wallet')
        before_balance_amount = before_balance[0]['amount']
        fee = await self.get_fees()
        fee = float(utils.base_amount(fee['average'], utils.DECIMAL))
        if (amount + fee) > float(before_balance_amount):
            raise Exception(
                'input asset amout is higher than current (asset balance - transfer fee)')

        try:
            await self.cosmos_client.make_transaction(self.get_private_key(), self.get_address(), fee_denom=asset['symbol'].lower(), memo=memo)
            self.cosmos_client.add_transfer(recipient, amount, denom=asset['symbol'].lower())
            Msg = self.cosmos_client.get_pushable()
            return await self.cosmos_client.do_transfer(Msg)
        except Exception as err:
            raise Exception(err)

    async def get_fees(self) -> dict:
        """Get the current fees

        :returns: The fees with three rates
        :rtype: dict
        """
        try:
            url = f'{self.client_url[self.network]["node"]}/thorchain/constants'
            client = http3.AsyncClient(timeout=10)
            response = await client.get(url)
            if  response.status_code == 200:
                res = json.loads(response.content.decode('utf-8'))['data']['int_64_values']['NativeTransactionFee']
                if not res or res < 0:
                    raise Exception(f'Invalid fee : {str(res)}')
                
                return {
                    "average" : res,
                    "fast" : res,
                    "fastest" : res,
                    "type" : "base"
                }
        except:
            return {
                    "average" : 0.02,
                    "fast" : 0.02,
                    "fastest" : 0.02,
                    "type" : "base"
                }


    async def build_deposit_tx(self , msg_native_tx : MsgNativeTx , node_url , chain_id) -> StdTx :
        try:
            network_chain_id = await get_chain_id(node_url)
            if not network_chain_id or chain_id != network_chain_id:
                raise Exception(f"Invalid network (asked : {chain_id} / returned : {network_chain_id})")
            
            url = f'{node_url}/thorchain/deposit'
            client = http3.AsyncClient(timeout=10)
            data = {
            "coins" : msg_native_tx.coins,
            "memo" : msg_native_tx.memo,
            "base_req" : {
                "chain_id" : chain_id,
                "from" : msg_native_tx.signer
            }  
            }
            response = await client.post(url=url, json=data)

            if response.status_code == 200:
                res = json.loads(response.content.decode('utf-8'))['value']
                fee : StdTxFee = None
                if res['fee']:
                    fee.gas = DEPOSIT_GAS_VALUE
                    fee.amount = res['fee']['amount']
                else:
                    fee.amount = []
                    fee.gas = DEPOSIT_GAS_VALUE
                unsigned_std_tx = StdTx(res['msg'] , fee ,[] ,'')

                return unsigned_std_tx
            else:
                raise Exception(response.text)

        except Exception as err:
            raise Exception(str(err))
        

    async def deposit(self, amount , memo , asset = {"chain" : "THOR", "symbol": "RUNE" , "ticker" : "RUNE"} , wallet_index = 0):
        try:
            asset_balance = await self.get_balance(self.get_address(wallet_index), [asset])
            
            fee = self.get_fees()["average"]

            if len(asset_balance) == 0 or float(asset_balance[0]['amount']) < (float(amount) + fee):
                raise Exception("insufficient funds")

            signer = self.get_address(wallet_index)
            coins = [MsgCoin(getDenomWithChain(asset), amount).to_obj()]

            msg_native_tx = message.msg_native_tx_from_json(coins, memo, signer)
            
            unsigned_std_tx = await self.build_deposit_tx(msg_native_tx,self.client_url[self.network]["node"] , self.get_chain_id())

            private_key = self.get_private_key(wallet_index)
            acc_address = frombech32(signer)

            result = await self.cosmos_client.sign_and_broadcast(unsigned_std_tx, private_key, acc_address)
            if not result['logs']:
                raise Exception("failed to broadcast transaction")
            else:
                return result

        except Exception as err:
            raise Exception(str(err))