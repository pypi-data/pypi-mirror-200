import pickle
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import hdf5plugin
import joblib
import ujson
import xarray as xr
import yaml
import zstandard as zstd


@dataclass
class Writer:
    @staticmethod
    def set_settings_file(settings_abs_path: str, settings: dict) -> None:
        with open(settings_abs_path, "w") as stream:
            yaml.safe_dump(settings, stream)

    @staticmethod
    def write_dataset(
        ds: xr.Dataset | xr.DataArray, abs_path: Path | str, group: str | None = None
    ) -> None:
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        if isinstance(ds, xr.DataArray):
            # make it a dataset
            ds = xr.Dataset({ds.name: ds}, attrs=ds.attrs)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        compression = {"compression": hdf5plugin.LZ4()}
        encoding = {var: compression for var in ds.data_vars}
        # if we write in a group, append
        mode = "w" if group is None else "a"
        ds.to_netcdf(
            path=abs_path,
            mode=mode,
            format="NETCDF4",
            group=group,
            engine="h5netcdf",
            encoding=encoding,
            unlimited_dims=None,
            compute=True,
            invalid_netcdf=False,
        )

    @staticmethod
    def pickle(variable: Any, abs_path: Path | str) -> None:
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        with open(abs_path, "wb") as handle:
            pickle.dump(variable, handle)

    @staticmethod
    def write_joblib(variable: Any, abs_path: Path | str) -> None:
        if isinstance(abs_path, str):
            abs_path = Path(abs_path)
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(variable, abs_path)

    @staticmethod
    def write_json_compressed(data: list | dict, output_file: Path | str) -> None:
        if isinstance(output_file, str):
            output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        json_bytes = ujson.dumps(data).encode("utf-8")
        compressor = zstd.ZstdCompressor(level=3)
        with open(output_file, "wb") as f:
            compressed_bytes = compressor.compress(json_bytes)
            f.write(compressed_bytes)

    @staticmethod
    def write_json_incremental(data: list | dict, output_file: Path | str) -> None:
        if isinstance(output_file, str):
            output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "a") as f:
            ujson.dump(data, f)
            f.write("\n")

    @staticmethod
    def write_bytes(data: bytes, output_file: Path | str) -> None:
        if isinstance(output_file, str):
            output_file = Path(output_file)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "wb") as f:
            f.write(data)
