class DerivePath:
    def __init__(self, index:int=0):

        self._mainnet = f"m/44'/145'/0'/0/{index}"
        self._testnet = f"m/44'/1'/0'/0/{index}"

    @property
    def mainnet(self):
        return self._mainnet

    @mainnet.setter
    def mainnet(self, mainnet):
        self._mainnet = mainnet

    @property
    def testnet(self):
        return self._testnet

    @testnet.setter
    def testnet(self, testnet):
        self._testnet = testnet

def get_derive_path(index: int = 0):
    return DerivePath(index=index)


class ClientUrl:
    def __init__(self , testnet , mainnet):
        self._testnet : str = testnet
        self._mainnet : str = mainnet

    @property
    def mainnet(self):
        return self._mainnet

    @mainnet.setter
    def mainnet(self, mainnet : str):
        self._mainnet = mainnet

    @property
    def testnet(self):
        return self._testnet

    @testnet.setter
    def testnet(self, testnet : str):
        self._testnet = testnet