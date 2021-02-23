import asyncio
from .interface import IXChainClient
from web3 import Web3, WebsocketProvider, HTTPProvider, Account
import json


class IEthereumClient:
    def get_contract(self, abi, address):
        pass

    def is_connected(self):
        pass


class Client(IEthereumClient, IXChainClient):
    def __init__(self, network: str, phrase: str):
        self.network = network
        self.phrase = phrase
        self.w3 = Web3(WebsocketProvider(network))
        Account.enable_unaudited_hdwallet_features()
        self.account = self.w3.eth.account.from_mnemonic(mnemonic=phrase)
        print(f'connected to wallet {self.account.address}')

    def is_connected(self):
        return self.w3.isConnected()

    def set_network(self, network: str):
        self.network = network
        self.w3 = Web3(WebsocketProvider(network))

    def get_network(self):
        return self.network

    def validate_address(self, address: str):
        pass

    def get_address(self):
        return self.account.address

    def set_phrase(self, phrase: str):
        """Set/Update a new phrase
        :param phrase: A new phrase
        :type phrase: str
        :returns: The address from the given phrase
        :raises: 'Invalid Phrase' if the given phrase is invalid
        """
        self.account = self.w3.eth.account.from_mnemonic(mnemonic=phrase)
        return self.get_address()

    def get_balance(self, address=None, asset=None, contract_abi=None, contract_address=None):
        if address:
            if asset:
                assert contract_abi
                assert contract_address
                token_contract = self.get_contract(contract_abi, contract_address)
                return token_contract.functions.balanceOf(address).call()
            return self.w3.fromWei(self.w3.eth.get_balance(address), 'ether')
        elif asset:
            assert contract_abi
            assert contract_address
            token_contract = self.get_contract(contract_abi, contract_address)
            return token_contract.functions.balanceOf(self.get_address()).call()
        return self.w3.fromWei(self.w3.eth.get_balance(self.get_address()), 'ether')

    def get_contract(self, abi, address):
        return self.w3.eth.contract(abi=abi, address=address)

    def get_fees(self):
        pass

    def transfer_ether(self, dest_addr, quantity):
        nonce = self.w3.eth.getTransactionCount(self.get_address())
        tx = {
            'nonce': nonce,
            'to': dest_addr,
            'value': self.w3.toWei(quantity, 'ether'),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei'),
        }
        signed_tx = self.account.sign_transaction(tx)
        tx_hash = self.w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return tx_hash

    def transfer_alt(self, dest_addr, quantity, contract):
        nonce = self.w3.eth.getTransactionCount(self.get_address())
        pass

    def write_contract(self, contract):
        pass


    def get_transaction_data(self, txId: str):
        return self.w3.eth.getTransaction(txId)

    def purge_client(self):
        pass