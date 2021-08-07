import pytest
from xchainpy_ethereum.models.asset import Asset


class TestAsset:
    def test_create_asset(self):
        asset = Asset('ETH', 'USDT', contract='0XA3910454BF2CB59B8B3A401589A3BACC5CA42306')
        assert asset.chain == 'ETH'
        assert asset.symbol == 'USDT'
        assert asset.contract == '0XA3910454BF2CB59B8B3A401589A3BACC5CA42306'

    def test_invalid_chain(self):
        with pytest.raises(Exception) as err:
            Asset('invalid chain', 'ETH')
        assert str(err.value) == "the chain is invalid"

    def test_asset_to_string(self):
        asset = Asset('ETH', 'USDT', contract='0XA3910454BF2CB59B8B3A401589A3BACC5CA42306')
        assert str(asset) == 'ETH.USDT:0XA3910454BF2CB59B8B3A401589A3BACC5CA42306'

    def test_asset_equal(self):
        asset = Asset('ETH', 'USDT', contract='0XA3910454BF2CB59B8B3A401589A3BACC5CA42306')
        asset2 = Asset('ETH', 'USDT', contract='0XA3910454BF2CB59B8B3A401589A3BACC5CA42306')
        assert asset == asset2