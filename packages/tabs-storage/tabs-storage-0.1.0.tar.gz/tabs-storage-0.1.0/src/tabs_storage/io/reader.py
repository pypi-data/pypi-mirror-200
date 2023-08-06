from __future__ import annotations

import pickle
from dataclasses import dataclass
from os import system
from pathlib import Path
from time import sleep
from typing import Any, Optional

import hdf5plugin
import joblib
import numpy as np
import pandas as pd
import polars as pl
import ujson
import xarray as xr
import yaml
import zstandard as zstd

xr.set_options(file_cache_maxsize=1)


@dataclass
class Reader:
    @classmethod
    def from_path(cls, folder: Path) -> Reader:
        # clean all the folder from the .DS_Store files
        Reader._clean_path(folder)
        return cls()

    @staticmethod
    def load_model(model_path: str | Path) -> Any:
        with open(model_path, "rb") as handle:
            model = pickle.load(handle)
        return model

    @staticmethod
    def load_joblib(abs_path: str | Path) -> Any:
        return joblib.load(abs_path)

    @staticmethod
    def load_settings_file(settings_abs_path: Path) -> dict:
        with open(settings_abs_path, "r") as stream:
            settings = yaml.safe_load(stream)
            return settings

    @staticmethod
    def _clean_path(path: Path) -> None:
        system(f"find {path} -name '.DS_Store' -type f -delete")

    @staticmethod
    def get_last_folder(path: Path) -> str:
        sub_paths = [sub_path.stem for sub_path in path.iterdir() if sub_path.is_dir()]
        return sorted(sub_paths)[-1] if sub_paths else ""

    @staticmethod
    def load_json(abs_path: str | Path) -> list[dict]:
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        if not abs_path.exists():
            raise FileNotFoundError(f"{abs_path} not found")
        with open(abs_path, "rb") as f:
            try:
                # Try to read the file as compressed JSON
                compressed_bytes = f.read()
                decompressor = zstd.ZstdDecompressor()
                json_bytes = decompressor.decompress(compressed_bytes)
                data = ujson.loads(json_bytes.decode("utf-8"))
            except zstd.ZstdError:
                # If the file is not compressed, read it as regular JSON
                with open(abs_path, "r") as f:
                    data = []
                    for line in f:
                        try:
                            data.append(ujson.loads(line))
                        except ujson.JSONDecodeError:
                            pass  # or handle the error
        return data

    @staticmethod
    def load_zip(abs_path: str | Path) -> pl.DataFrame:
        # if any data is numeric in the first line, then assume
        # there is no header.

        # Load the file with the default parameters to check if it has a header
        df_no_header = pd.read_csv(abs_path, header=None, nrows=1, compression="zip")
        first_row = df_no_header.iloc[0]

        has_header = (
            not first_row.apply(
                lambda x: isinstance(x, (int, float, np.integer, np.floating))
            )
            .any()
            .any()
        )
        # Load the file with the correct header parameter
        if has_header:
            df = pd.read_csv(abs_path)
        else:
            column_names = ["column_{}".format(i) for i in range(df_no_header.shape[1])]
            df = pd.read_csv(abs_path, names=column_names, header=None)

        pl_df = pl.from_pandas(df)
        return pl_df

    @staticmethod
    def load_dataset(
        abs_path: Path | str, group: Optional[str] = None
    ) -> xr.Dataset | None:
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        Reader._clean_path(abs_path.parent)
        try:
            ds = xr.load_dataset(
                abs_path,
                engine="h5netcdf",
                group=group,
            )
        except ValueError as e:
            c1 = "Invalid location identifier" in str(e)
            c2 = "Invalid object identifier" in str(e)
            if c1 or c2:
                print(f"retrying {abs_path}...")
                sleep(0.1)
                ds = Reader.load_dataset(abs_path, group=group)
        except AttributeError as e:
            c2 = "'NoneType' object has no attribute '_h5file'" in str(e)
            if c2:
                print(f"retrying {abs_path}...")
                sleep(0.1)
                ds = Reader.load_dataset(abs_path, group=group)
        except OSError as e:
            if str(e) == "Unable to open file (bad object header version number)":
                abs_path.unlink()
                ds = None
            ds = None
        return ds

    @staticmethod
    def load_multi_dates(
        dir_name: Path | str,
        dates: list[str],
        group: Optional[str] = "",
        prefix: Optional[str] = "",
    ) -> xr.Dataset:
        if isinstance(dir_name, str):
            dir_name = Path(dir_name)
        datasets = {}
        for date in dates:
            abs_path = dir_name / f"{prefix}{date}.h5"
            try:
                ds = Reader.load_dataset(abs_path, group)
                datasets[date] = ds
            except FileNotFoundError:
                print(f"{abs_path} is missing")
                continue

        # remove files that were not available
        datasets = {
            date: ds for date, ds in datasets.items() if isinstance(ds, xr.Dataset)
        }
        sorted_dates = sorted(list(datasets.keys()))
        ds = xr.concat(
            [datasets[date] for date in sorted_dates],
            dim="index" if "index" in datasets[sorted_dates[0]].dims else "opp",
        )

        return ds
