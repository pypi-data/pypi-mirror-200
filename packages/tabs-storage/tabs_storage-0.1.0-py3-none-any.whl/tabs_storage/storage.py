from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import xarray as xr
from immutables import Map
from packaging.version import Version
from tabs_settings.config.data_segment import DataSegment
from tabs_settings.config.learn import LearnConfig
from tabs_settings.config.storage import PathFormatType, StorageConfig
from tabs_settings.config.trading_pair import TradingPair

from tabs_storage.home import Home
from tabs_storage.io.reader import Reader
from tabs_storage.io.writer import Writer

Serializable = bytes | list[dict] | xr.Dataset


@dataclass(frozen=True)
class Storage:
    home: Home
    storage_config: StorageConfig
    writing_version: Version
    reading_versions: Map[DataSegment, Version] = Map()

    @classmethod
    def from_settings(
        cls,
        home_type: str,
        settings: dict,
        writing_version: Version,
        reading_versions: Map[DataSegment, Version],
    ) -> Storage:
        return cls(
            Home.from_settings(home_type),
            StorageConfig.from_yaml(settings),
            writing_version,
            reading_versions,
        )

    def resolve_path(
        self,
        version: Version,
        data_segment: DataSegment,
        date: str | None,
        trading_pair: TradingPair | None = None,
        learn: LearnConfig | None = None,
    ) -> Path:
        # handle extension resolution
        if data_segment is DataSegment.RAW_TRADES:
            assert trading_pair is not None
            extension = self.storage_config.extension[data_segment][
                trading_pair.exchange
            ]
        else:
            extension = self.storage_config.extension[data_segment]

        # handle path resolution based on data segment
        if data_segment.is_market_data:
            assert trading_pair is not None
            relative_path = (
                self.storage_config.path_format[PathFormatType.RAW_DATA]
                .format(
                    version=version,
                    trading_pair=trading_pair.pair_name_maybe_with_maturity,
                    data_segment=data_segment.value,
                    exchange=trading_pair.exchange.name,
                    asset_type=trading_pair.asset_type.name,
                    date=date,
                    extension=extension,
                )
                .lower()
            )

        elif data_segment.is_oppfile:
            assert learn is not None
            relative_path = self.storage_config.path_format[
                PathFormatType.OPPFILE
            ].format(
                version=version,
                basket=learn.basket.name,
                data_segment=data_segment.value,
                date=date,
                extension=extension,
            )

        else:
            assert learn is not None
            if (
                data_segment is DataSegment.MODEL
                or data_segment is DataSegment.SCORE_EVALUATION
            ):
                date = learn.partition.partition_date

            relative_path = self.storage_config.path_format[
                PathFormatType.LEARN
            ].format(
                version=version,
                basket=learn.basket.name,
                data_segment=data_segment.value,
                date=date,
                extension=extension,
                rolling_learn_id=learn.roll_name,
                learn_id=learn.name,
            )

        return self.home.home_path / relative_path

    def exists(
        self,
        data_segment: DataSegment,
        date: str,
        is_reading: bool,
        trading_pair: TradingPair | None = None,
        learn: LearnConfig | None = None,
    ) -> bool:
        version = (
            self.reading_versions[data_segment] if is_reading else self.writing_version
        )
        abs_path = self.home.home_path / self.resolve_path(
            version, data_segment, date, trading_pair, learn
        )
        return abs_path.exists()

    def load(
        self,
        data_segment: DataSegment,
        date: str | None = None,
        trading_pair: TradingPair | None = None,
        learn: LearnConfig | None = None,
    ) -> Any:
        resolved_abs_path = self.resolve_path(
            self.reading_versions[data_segment],
            data_segment,
            date,
            trading_pair,
            learn,
        )
        suffix = "".join(resolved_abs_path.suffixes)

        if suffix == ".h5":
            data = Reader.load_dataset(
                resolved_abs_path,
            )
        elif suffix in {".json", ".json.compressed"}:
            data = Reader.load_json(
                resolved_abs_path,
            )
        elif suffix == ".zip":
            data = Reader.load_zip(
                resolved_abs_path,
            )
        elif suffix == ".joblib":
            data = Reader.load_joblib(resolved_abs_path)

        return data

    def save(
        self,
        data: Serializable,
        data_segment: DataSegment,
        date: str | None = None,
        trading_pair: TradingPair | None = None,
        learn: LearnConfig | None = None,
    ):
        resolved_abs_path = self.resolve_path(
            self.writing_version,
            data_segment,
            date,
            trading_pair,
            learn,
        )
        suffix = "".join(resolved_abs_path.suffixes)

        if suffix == ".h5":
            assert isinstance(data, xr.Dataset)
            Writer.write_dataset(data, resolved_abs_path)
        elif suffix == ".json":
            assert isinstance(data, list | dict)
            Writer.write_json_incremental(
                data,
                resolved_abs_path,
            )
        elif suffix == ".json.compressed":
            assert isinstance(data, list | dict)
            Writer.write_json_compressed(
                data,
                resolved_abs_path,
            )
        elif suffix == ".zip":
            assert isinstance(data, bytes)
            Writer.write_bytes(
                data,
                resolved_abs_path,
            )
        elif suffix == ".joblib":
            Writer.write_joblib(
                data,
                resolved_abs_path,
            )
