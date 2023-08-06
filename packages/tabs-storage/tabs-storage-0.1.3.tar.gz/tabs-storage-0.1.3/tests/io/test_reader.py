import numpy as np
import pandas as pd
import pytest
import ujson
import xarray as xr
import zstandard as zstd
from tabs_storage.io.reader import Reader
from tabs_storage.io.writer import Writer


def test_clean_path(tmp_path):
    ds_store_path = tmp_path / ".DS_Store"
    ds_store_path.touch()
    assert ds_store_path.exists()
    Reader._clean_path(tmp_path)
    assert not ds_store_path.exists()


def testget_last_folder(tmp_path):
    sub_dir_1 = tmp_path / "sub_dir_1"
    sub_dir_1.mkdir()
    sub_dir_2 = tmp_path / "sub_dir_2"
    sub_dir_2.mkdir()
    sub_dir_3 = tmp_path / "sub_dir_3"
    sub_dir_3.mkdir()
    last_folder = Reader.get_last_folder(tmp_path)
    assert last_folder == "sub_dir_3"


def testget_last_folder_empty(tmp_path):
    last_folder = Reader.get_last_folder(tmp_path)
    assert last_folder == ""


@pytest.fixture
def existing_dates():
    return ["20220101", "20220102"]


@pytest.fixture
def mock_datasets(tmp_path, existing_dates):
    for date in existing_dates:
        ds = xr.Dataset(
            {"test": xr.DataArray(np.array([1]), coords={"index": [0]}, dims=["index"])}
        )
        Writer.write_dataset(ds, tmp_path / f"{date}.h5")
    return tmp_path


def test_load_multi_dates(mock_datasets, existing_dates):
    non_existing_date = "20220103"
    dates = existing_dates + [non_existing_date]
    ds = Reader.load_multi_dates(mock_datasets, dates)
    # check that the missing date have been ignored
    assert isinstance(ds, xr.Dataset)


@pytest.fixture(scope="module")
def json_data():
    return [
        {"name": "John Doe", "age": 35},
        {"name": "Jane Doe", "age": 30},
        {"name": "Bob Smith", "age": 45},
    ]


def test_read_json_file(tmp_path, json_data):
    json_file = tmp_path / "test.json"
    compressed_file = tmp_path / "test.zst"
    # Write JSON data to file
    with json_file.open("w") as f:
        for d in json_data:
            f.write(ujson.dumps(d) + "\n")

    # Compress JSON data and write to file
    compressor = zstd.ZstdCompressor()
    compressed_bytes = compressor.compress(ujson.dumps(json_data).encode("utf-8"))
    with compressed_file.open("wb") as f:
        f.write(compressed_bytes)

    # Test reading the JSON file
    assert Reader.load_json(json_file) == json_data

    # Test reading the compressed JSON file
    assert Reader.load_json(compressed_file) == json_data

    # Test reading a non-existent file
    with pytest.raises(FileNotFoundError):
        Reader.load_json(tmp_path / "non_existent.json")


def create_test_csv(zip_file_path, has_header):
    df = pd.DataFrame(
        {"A": [1, 2, 3], "B": [4, 5, 6], "C": [True, True, False]},
        columns=["A", "B", "C"],
    )
    if not has_header:
        # Save the CSV file without headers
        df.to_csv(zip_file_path, index=False, header=False, compression="zip")
    else:
        # Save the CSV file with headers
        df.to_csv(zip_file_path, index=False, compression="zip")


@pytest.mark.parametrize("has_header", [True, False])
def test_load_zip(tmp_path, has_header):
    # Create a test CSV file with or without headers
    zip_file_path = str(tmp_path / "test.zip")
    create_test_csv(zip_file_path, has_header=has_header)

    # Load the CSV file using the load_zip() function
    pl_df = Reader.load_zip(zip_file_path)

    # Check that the DataFrame has the correct shape and column names
    assert pl_df.shape == (3, 3)
    if has_header:
        assert pl_df.columns == ["A", "B", "C"]
    else:
        assert pl_df.columns == ["column_0", "column_1", "column_2"]


def test_load_joblib(tmp_path):
    # Create a test DataFrame
    df = pd.DataFrame(
        {"A": [1, 2, 3], "B": [4, 5, 6], "C": [True, True, False]},
        columns=["A", "B", "C"],
    )
    joblib_file_path = str(tmp_path / "test.joblib")
    Writer.write_joblib(df, joblib_file_path)
    pl_df = Reader.load_joblib(joblib_file_path)
    pd.testing.assert_frame_equal(pl_df, df)
