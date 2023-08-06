import pytest
import xarray as xr
import yaml
from immutables import Map
from packaging.version import Version
from tabs_settings.config.basket import Basket
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.storage import StorageConfig
from tabs_settings.config.trading_pair import TradingPair
from tabs_storage.home import Home
from tabs_storage.storage import Storage


@pytest.fixture
def home(tmp_path):
    return Home.from_settings("test", tmp_path)


@pytest.fixture
def storage_config():
    yaml_str = """ 
    path_format:
        raw_data: data/raw_data/{version}/{exchange}/{asset_type}/{trading_pair}/{data_segment}/{date}.{extension}
        oppfile: data/learn/{version}/dataset/{basket}/{data_segment}/{date}.{extension}
        learn: data/learn/{version}/{rolling_learn_id}/{learn_id}/{basket}/{data_segment}/{date}.{extension}

    extension:
        # raw data
        raw_trades:
            binance: zip
            kraken: json.compressed
            okx: zip
        trades: h5
        raw_price_level_book: json
        compressed_price_level_book: json.compressed
        price_level_book: h5

        # learn
        backtest: h5
        tactic_tuning: h5
        scores_metrics: h5
        scores: h5
        model: h5

        # oppfile
        oppfile_triggers: h5
        oppfile_signal: h5
        oppfile_enhanced: h5
        oppfile_header: h5
        oppfile_price_level_book: h5
    """
    # load yaml settings into a dict
    data = yaml.safe_load(yaml_str)
    return StorageConfig.from_yaml(data)


@pytest.fixture
def basket():
    trading_pair_1 = TradingPair.from_parameters(
        base_asset="BTC",
        quote_asset="USDT",
        asset_type="spot",
        exchange="binance",
    )
    trading_pair_2 = TradingPair.from_parameters(
        base_asset="ETH",
        quote_asset="USDT",
        asset_type="spot",
        exchange="binance",
    )
    return Basket(frozenset([trading_pair_1, trading_pair_2]))


@pytest.fixture
def reading_versions():
    return Map(
        {
            DataSegment.RAW_TRADES: Version("0.1.0"),
            DataSegment.TRADES: Version("0.1.0"),
            DataSegment.RAW_PRICE_LEVEL_BOOK: Version("0.1.0"),
            DataSegment.COMPRESSED_PRICE_LEVEL_BOOK: Version("0.1.0"),
            DataSegment.PRICE_LEVEL_BOOK: Version("0.1.0"),
            DataSegment.OPPFILE_ENHANCED: Version("0.1.0"),
        }
    )


@pytest.fixture
def storage(storage_config, home, reading_versions):
    return Storage(home, storage_config, Version("0.1.0"), reading_versions)


@pytest.mark.parametrize(
    "version, data_segment, date, trading_pair, expected",
    [
        (
            Version("0.1.0"),
            DataSegment.RAW_TRADES,
            "20210101",
            TradingPair.from_parameters(
                base_asset="BTC",
                quote_asset="USDT",
                asset_type="spot",
                exchange="binance",
            ),
            "data/raw_data/0.1.0/binance/spot/btcusdt/raw_trades/20210101.zip",
        ),
        (
            Version("0.1.0"),
            DataSegment.RAW_PRICE_LEVEL_BOOK,
            "20210101",
            TradingPair.from_parameters(
                base_asset="BTC",
                quote_asset="USDT",
                asset_type="spot",
                exchange="binance",
            ),
            "data/raw_data/0.1.0/binance/spot/btcusdt/raw_price_level_book/20210101.json",
        ),
        (
            Version("0.1.0"),
            DataSegment.RAW_PRICE_LEVEL_BOOK,
            "20210101",
            TradingPair.from_parameters(
                base_asset="BTC",
                quote_asset="USDT",
                asset_type="future",
                exchange="binance",
                maturity="20230331",
            ),
            "data/raw_data/0.1.0/binance/future/btcusdt_20230331/raw_price_level_book/20210101.json",
        ),
    ],
)
def test_resolve_path_raw_data(
    storage, version, data_segment, date, trading_pair, expected
):
    assert (
        storage.resolve_path(version, data_segment, date, trading_pair)
        == storage.home.home_path / expected
    )


@pytest.mark.parametrize(
    "version, data_segment, date, expected",
    [
        (
            Version("0.1.0"),
            DataSegment.MODEL,
            "20210101",
            "data/learn/0.1.0/test_roll/test_roll/test-20220420_40/test/model/20210101.h5",
        ),
        (
            Version("0.1.0"),
            DataSegment.SCORES,
            "20210101",
            "data/learn/0.1.0/test_roll/test_roll/test-20220420_40/test/scores/20210101.h5",
        ),
        (
            Version("0.1.0"),
            DataSegment.SCORES_METRICS,
            "20210101",
            "data/learn/0.1.0/test_roll/test_roll/test-20220420_40/test/scores_metrics/20210101.h5",
        ),
        (
            Version("0.1.0"),
            DataSegment.TACTIC_TUNING,
            "20210101",
            "data/learn/0.1.0/test_roll/test_roll/test-20220420_40/test/tactic_tuning/20210101.h5",
        ),
    ],
)
def test_resolve_path_learn(storage, version, data_segment, date, learn, expected):
    assert (
        storage.resolve_path(version, data_segment, date, learn=learn)
        == storage.home.home_path / expected
    )


@pytest.mark.parametrize(
    "version, data_segment, date, expected",
    [
        (
            Version("0.1.0"),
            DataSegment.OPPFILE_TRIGGERS,
            "20210101",
            "data/learn/0.1.0/dataset/test/oppfile_triggers/20210101.h5",
        ),
    ],
)
def test_resolve_path_oppfile(storage, version, data_segment, date, learn, expected):
    assert (
        storage.resolve_path(version, data_segment, date, learn=learn)
        == storage.home.home_path / expected
    )


@pytest.mark.parametrize(
    "data, data_segment, date, trading_pair, learn",
    [
        (
            [{"test": 1}],
            DataSegment.RAW_TRADES,
            "20210101",
            TradingPair.from_parameters(
                base_asset="BTC",
                quote_asset="USDT",
                asset_type="spot",
                exchange="kraken",
            ),
            None,
        ),
        (
            xr.Dataset({"test": xr.DataArray(1)}),
            DataSegment.TRADES,
            "20210101",
            TradingPair.from_parameters(
                base_asset="BTC",
                quote_asset="USDT",
                asset_type="spot",
                exchange="kraken",
            ),
            None,
        ),
        # (
        #     xr.Dataset({"test": xr.DataArray(1)}),
        #     DataSegment.OPPFILE_TRIGGERS,
        #     "20210101",
        #     None,
        #     Basket(
        #         name="test",
        #         trading_pairs=frozenset(
        #             {
        #                 TradingPair.from_parameters(
        #                     base_asset="BTC",
        #                     quote_asset="USDT",
        #                     asset_type="spot",
        #                     exchange="kraken",
        #                 ),
        #                 TradingPair.from_parameters(
        #                     base_asset="BTC",
        #                     quote_asset="USDT",
        #                     asset_type="spot",
        #                     exchange="kraken",
        #                 ),
        #             }
        #         ),
        #     ),
        # ),
        # (
        #     b"""PK\x03\x04\x14\x00\x00""",  # issue: not a zip file
        #     DataSegment.RAW_TRADES,
        #     "20210101",
        #     TradingPair.from_parameters(
        #         base_asset="BTC",
        #         quote_asset="USDT",
        #         asset_type="spot",
        #         exchange="binance",
        #     ),
        #     None,
        # ),
    ],
)
def test_save_exists_read_raw_data(
    storage, data, data_segment, date, trading_pair, learn
):
    assert not storage.exists(
        data_segment,
        date,
        is_reading=False,
        trading_pair=trading_pair,
        learn=learn,
    )
    storage.save(data, data_segment, date, trading_pair, learn)
    assert storage.exists(
        data_segment,
        date,
        is_reading=False,
        trading_pair=trading_pair,
        learn=learn,
    )
    assert storage.load(data_segment, date, trading_pair, learn) == data
