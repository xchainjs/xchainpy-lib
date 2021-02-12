class DerivePath:
    def __init__(self, index:int=0):

        self._mainnet = f"84'/0'/0'/0/{index}"
        self._testnet = f"84'/1'/0'/0/{index}"

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