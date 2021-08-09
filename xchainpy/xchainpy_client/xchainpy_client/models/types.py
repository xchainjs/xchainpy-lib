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

class FeeRates:
    def __init__(self, fast, fastest, average):
        """
        :param fast: fast
        :type fast: float
        :param fastest: fastest 
        :type fastest: float
        :param average: average 
        :type average: float
        """
        self._fast = fast
        self._fastest = fastest
        self._average = average

    @property
    def fast(self):
        return self._fast

    @fast.setter
    def fast(self, fast):
        self._fast = fast

    @property
    def fastest(self):
        return self._fastest

    @fastest.setter
    def fastest(self, fastest):
        self._fastest = fastest

    @property
    def average(self):
        return self._average

    @average.setter
    def average(self, average):
        self._average = average

class Fees:
    def __init__(self, fast, fastest, average):
        """
        :param fast: fast
        :type fast: float
        :param fastest: fastest 
        :type fastest: float
        :param average: average 
        :type average: float
        """
        self._fast = fast
        self._fastest = fastest
        self._average = average

    @property
    def fast(self):
        return self._fast

    @fast.setter
    def fast(self, fast):
        self._fast = fast

    @property
    def fastest(self):
        return self._fastest

    @fastest.setter
    def fastest(self, fastest):
        self._fastest = fastest

    @property
    def average(self):
        return self._average

    @average.setter
    def average(self, average):
        self._average = average

class FeesWithRates:
    def __init__(self, fees, rates):
        """
        :param fees: fees
        :type fees: Fees
        :param rates: rates 
        :type rates: float
        """
        self._fees = fees
        self._rates = rates

    @property
    def fees(self):
        return self._fees

    @fees.setter
    def fees(self, fees):
        self._fees = fees

    @property
    def rates(self):
        return self._rates

    @rates.setter
    def rates(self, rates):
        self._rates = rates

