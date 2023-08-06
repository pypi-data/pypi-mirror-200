import pickle
from pathlib import Path

import pytest
import xarray as xr
from tabs_storage.io.reader import Reader
from tabs_storage.io.writer import Writer


@pytest.fixture
def dataset():
    data = {
        "a": (["x", "y"], [[1, 2, 3], [4, 5, 6]]),
        "b": (["x", "y"], [[7, 8, 9], [10, 11, 12]]),
    }
    return xr.Dataset(data)


def test_save_dataset(dataset, tmp_path):
    group = "test"
    abs_path = Path(tmp_path / "test.nc")
    Writer.write_dataset(dataset, abs_path, group)
    assert abs_path.exists()
    loaded = xr.open_dataset(abs_path, group=group)
    xr.testing.assert_identical(dataset, loaded)


@pytest.mark.parametrize(
    "variable",
    [({"a": 1, "b": 2})],
)
def test_pickle(variable, tmp_path):
    abs_path = Path(tmp_path / "test.pickle")
    Writer.pickle(variable, abs_path)
    assert (abs_path).exists()
    with open(abs_path, "rb") as handle:
        loaded_variable = pickle.load(handle)
    assert variable == loaded_variable


def test_save_compressed_json(tmp_path):
    # Create some data to save
    data = [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 25},
        {"name": "Charlie", "age": 40},
    ]

    # Save the data using the method under test
    output_file = tmp_path / "data.json.zst"
    Writer.write_json_compressed(data, output_file)

    # Check that the output file exists
    assert output_file.exists()

    # Load the saved data using the read_compressed_json method and check that
    # it matches the original data
    saved_data = Reader.load_json(output_file)
    assert saved_data == data


@pytest.mark.parametrize(
    "settings, expected_output",
    [
        ({"key1": "value1", "key2": "value2"}, "key1: value1\nkey2: value2\n"),
        ({"key3": "value3", "key4": "value4"}, "key3: value3\nkey4: value4\n"),
    ],
)
def test_set_settings_file(tmp_path, settings, expected_output):
    temp_settings_file = tmp_path / "settings.yaml"
    Writer.set_settings_file(temp_settings_file, settings)
    with open(temp_settings_file, "r") as f:
        assert f.read() == expected_output
