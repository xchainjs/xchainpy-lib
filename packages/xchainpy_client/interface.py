class IXChainClient():

    def set_network(self, network: str):
        pass
    def get_network(self):
        pass
    def validate_address(self, address: str): 
        pass
    def get_address(self): 
        pass
    def set_phrase(self, phrase: str):
        pass
    def get_balance(self, address: str, asset):
        pass
    def get_transaction_data(self, txId: str):
        pass
    def get_fees(self):
        pass
    def transfer(self, txParams):
        pass
    def purge_client(self):
        pass