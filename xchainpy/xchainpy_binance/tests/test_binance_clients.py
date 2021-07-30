import pytest
from xchainpy_client.models.types import Network, XChainClientParams
from xchainpy_binance.client import Client
from xchainpy_util.asset import Asset
from xchainpy_client.models import tx_types

class TestBinanceClient:

    # Note: This phrase is created by https://iancoleman.io/bip39/ and will never been used in a real-world
    phrase = 'rural bright ball negative already grass good grant nation screen model pizza'
    mainnetaddress_path0 = 'bnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9e738vr'
    mainnetaddress_path1 = 'bnb1vjlcrl5d9t8sexzajsr57taqmxf6jpmgng3gmn'

    testnetaddress_path0 = 'tbnb1zd87q9dywg3nu7z38mxdcxpw8hssrfp9htcrvj'
    testnetaddress_path1 = 'tbnb1vjlcrl5d9t8sexzajsr57taqmxf6jpmgaacvmz'
    bnb_asset = Asset('BNB', 'BNB', 'BNB')

    phraseForTX = 'wheel leg dune emerge sudden badge rough shine convince poet doll kiwi sleep labor hello'
    testnetaddress_path0ForTx = 'tbnb1t95kjgmjc045l2a728z02textadd98yt339jk7'
    
    transfer_amount = 0.0001


    @pytest.fixture
    def client(self):
        self.client = Client(XChainClientParams(network=Network.Mainnet, phrase=self.phrase))
        yield
        self.client.purge_client()

    def test_empty_wallet_main(self):
        client = Client(XChainClientParams(network=Network.Mainnet, phrase=self.phrase))
        address_main = client.get_address()
        assert address_main == self.mainnetaddress_path0

    def test_empty_wallet_test(self):
        client = Client(XChainClientParams(network=Network.Testnet, phrase=self.phrase))
        address_test = client.get_address()
        assert address_test == self.testnetaddress_path0

    def test_invalid_phrase(self):
        with pytest.raises(Exception) as err:
            assert Client(XChainClientParams(network=Network.Testnet, phrase='invalid phrase'))
        assert str(err.value) == "invalid phrase"

    def test_update_net(self, client):
        self.client.set_network('testnet')
        assert self.client.get_network() == 'testnet'
        assert self.client.get_address() == self.testnetaddress_path0

    def test_right_address(self, client):
        assert self.client.get_address() == self.mainnetaddress_path0
        assert self.client.get_address(1) == self.mainnetaddress_path1
        self.client.set_network('testnet')
        assert self.client.get_address() == self.testnetaddress_path0
        assert self.client.get_address(1) == self.testnetaddress_path1

    def test_set_phrase_return_address(self, client):
        assert self.client.set_phrase(self.phrase) == self.mainnetaddress_path0
        self.client.set_network('testnet')
        assert self.client.set_phrase(self.phrase) == self.testnetaddress_path0

    def test_validate_address(self, client):
        assert self.client.validate_address(self.mainnetaddress_path0) == True

    def test_validate_address_false_address(self, client):
        assert self.client.validate_address(self.mainnetaddress_path0 + '1') == False

    @pytest.mark.asyncio
    async def test_has_no_balances(self, client):
        assert await self.client.get_balance(address='bnb1v8cprldc948y7mge4yjept48xfqpa46mmcrpku') == []

    @pytest.mark.asyncio
    async def test_has_balances(self, client):
        self.client.set_network('testnet')
        assert await self.client.get_balance(address=self.testnetaddress_path0)

    @pytest.mark.asyncio
    async def test_balance_has_correct_asset(self, client):
        self.client.set_network('testnet')
        balance = await self.client.get_balance(self.testnetaddress_path0, self.bnb_asset)
        assert str(balance[0].asset) == str(self.bnb_asset)
        assert balance[0].amount

    @pytest.mark.asyncio
    async def test_get_transfer_fees(self, client):
        self.client.set_network('testnet')
        fee = await self.client.get_fees()
        assert fee.average
        assert fee.fast
        assert fee.fastest

    @pytest.mark.asyncio
    async def test_get_multi_send_fees(self, client):
        fee = await self.client.get_multi_send_fees()
        assert fee.average
        assert fee.fast
        assert fee.fastest

    @pytest.mark.asyncio
    async def test_get_single_and_multi_fees(self, client):
        fee = await self.client.get_single_and_multi_fees()
        assert fee['multi'].average 
        assert fee['multi'].fast
        assert fee['multi'].fastest
        assert fee['single'].average
        assert fee['single'].fast
        assert fee['single'].fastest

    @pytest.mark.asyncio
    async def test_should_broadcast_transfer(self, client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phraseForTX)
        assert self.client.get_address() == self.testnetaddress_path0ForTx
        before_balance = await self.client.get_balance(self.testnetaddress_path0ForTx)
        assert len(before_balance) == 1
        before_balance_amount = before_balance[0].amount
        await self.client.transfer(tx_types.TxParams(asset=self.bnb_asset, amount=self.transfer_amount, recipient=self.testnetaddress_path0ForTx))
        after_balance = await self.client.get_balance(self.testnetaddress_path0ForTx)
        after_balance_amount = after_balance[0].amount
        # assert round((float(before_balance_amount) - float(after_balance_amount)) * 10**8) == round((await self.client.get_fees()).average * 10 ** 8)

    @pytest.mark.asyncio
    async def test_should_raise_exception_if_input_amount_higher_than_balance(self , client):
        self.client.set_network('testnet')
        self.client.set_phrase(self.phraseForTX)
        before_balance = await self.client.get_balance(self.testnetaddress_path0ForTx)
        before_balance_amount = before_balance[0].amount
        send_amount = float(before_balance_amount) + 1
        with pytest.raises(Exception) as err:
            await self.client.transfer(tx_types.TxParams(asset=self.bnb_asset, amount=send_amount, recipient=self.testnetaddress_path0ForTx))
        assert str(err.value) == "input asset amout is higher than current (asset balance - transfer fee)"

    @pytest.mark.asyncio
    async def test_has_empty_tx_history(self, client):
        self.client.set_network('testnet')
        address = self.client.set_phrase('nose link choose blossom social craft they better render provide escape talk')
        params = tx_types.TxHistoryParams(address=address, limit=1)
        transactions = await self.client.get_transactions(params)
        assert transactions
        assert len(transactions['tx']) == 0

    @pytest.mark.asyncio
    async def test_get_transactions(self, client):
        self.client.set_network('testnet')
        params = tx_types.TxHistoryParams(address=self.testnetaddress_path0ForTx, limit=1)
        transactions = await self.client.get_transactions(params)
        assert transactions
        assert len(transactions['tx']) == 1 or 0
        if transactions['total'] > 0:
            assert isinstance(transactions['tx'][0], tx_types.TX)

    @pytest.mark.asyncio
    async def test_get_transaction_data(self, client):
        self.client.set_network('testnet')
        try:
            params = tx_types.TxHistoryParams(address=self.testnetaddress_path0ForTx, limit=1)
            transactions = await self.client.get_transactions(params)
            transaction = await self.client.get_transaction_data(transactions['tx'][0].tx_hash)
            assert transaction
            assert isinstance(transaction, tx_types.TX)
        except Exception as err:
            assert str(err) == 'list index out of range' # there is not any transaction in the last 3 months for this address

    def test_should_return_valid_explorer_url(self, client):
        assert self.client.get_explorer_url() == 'https://explorer.binance.org'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_url() == 'https://testnet-explorer.binance.org'

    def test_should_retrun_valid_explorer_address_url(self, client):
        assert self.client.get_explorer_address_url('anotherTestAddressHere') == 'https://explorer.binance.org/address/anotherTestAddressHere'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_address_url('testAddressHere') == 'https://testnet-explorer.binance.org/address/testAddressHere'

    def test_should_retrun_valid_explorer_tx_url(self, client):
        assert self.client.get_explorer_tx_url('anotherTestTxHere') == 'https://explorer.binance.org/tx/anotherTestTxHere'
        self.client.set_network(Network.Testnet)
        assert self.client.get_explorer_tx_url('testTxHere') == 'https://testnet-explorer.binance.org/tx/testTxHere'

    # @pytest.mark.asyncio
    # async def test_multi_send(self, client):
    #     self.client.set_network('testnet')
    #     self.client.set_phrase(self.phraseForTX)
    #     assert self.client.get_address() == self.testnetaddressForTx
    #     before_balance = await self.client.get_balance()
    #     assert len(before_balance) == 1
    #     before_balance_amount = before_balance[0].amount

    #     coins = [Coin(self.bnb_asset, self.transfer_amount), Coin(Asset.from_str('BNB.BNB'), self.transfer_amount)]
    #     tx_hash = await self.client.multi_send(coins, 'tbnb185tqzq3j6y7yep85lncaz9qeectjxqe5054cgn')

    #     after_balance = await self.client.get_balance()
    #     after_balance_amount = after_balance[0].amount
    #     assert round((float(before_balance_amount) - float(after_balance_amount)) * 10**8) == round(self.multi_tx_fee * 10 ** -8, 8)