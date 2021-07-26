import enum

class Network(enum.Enum):
    Mainnet = 'mainnet'
    Testnet = 'testnet'

class RootDerivationPaths:
    def __init__(self, mainnet, testnet):
        """
        :param mainnet: mainnet
        :type mainnet: str
        :param testnet: testnet 
        :type testnet: str
        """
        self._mainnet = mainnet
        self._testnet = testnet

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


class XChainClientParams:
    def __init__(self, network:Network=None, phrase=None, root_derivation_paths=None):
        """
        :param network: network
        :type network: str
        :param phrase: phrase 
        :type phrase: str
        :param root_derivation_paths: root_derivation_paths 
        :type root_derivation_paths: RootDerivationPaths
        """
        if network:
            if type(network) is Network:
                self._network = network.value
            elif type(network) is str and network in ['mainnet', 'MAINNET', 'testnet', 'TESTNET']:
                self._network = network.lower()
            else:
                raise Exception("Invalid network")
        else:
            self._network = network

        self._phrase = phrase
        self._root_derivation_paths = root_derivation_paths

    @property
    def network(self):
        return self._network

    @network.setter
    def network(self, network):
        self._network = network

    @property
    def phrase(self):
        return self._phrase

    @phrase.setter
    def phrase(self, phrase):
        self._phrase = phrase

    @property
    def root_derivation_paths(self):
        return self._root_derivation_paths

    @root_derivation_paths.setter
    def root_derivation_paths(self, root_derivation_paths):
        self._root_derivation_paths = root_derivation_paths