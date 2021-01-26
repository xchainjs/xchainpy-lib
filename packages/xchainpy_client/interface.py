class IXChainClient():

    def setNetwork(self, network: str):
        pass
    def getNetwork(self):
        pass
    def getExplorerUrl(self):
        pass
    def getExplorerAddressUrl(self, address: str):
        pass
    def getExplorerTxUrl(self, txID: str): 
        pass
    def validateAddress(self, address: str): 
        pass
    def getAddress(self): 
        pass
    def setPhrase(self, phrase: str):
        pass
    def getBalance(self, address: str, asset):
        pass
    def getTransactions(self, txHistoryParams):
        pass
    def getTransactionData(self, txId: str):
        pass
    def getFees(self):
        pass
    def transfer(self, txParams):
        pass
    def purgeClient(self):
        pass