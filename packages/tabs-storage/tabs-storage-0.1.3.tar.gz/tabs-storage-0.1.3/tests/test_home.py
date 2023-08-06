from pathlib import Path

import pytest
from tabs_storage.home import Home, HomeType


@pytest.fixture
def home_config():
    return {
        "local": "/Users/alexis/tabs",
        "hdd": "/Volumes/Elements/tabs",
        "bucket": "/mnt/disks/tabs",
        "google": "/home/alexis",
    }


@pytest.mark.parametrize(
    "home_type_str, path, expected_type",
    [
        ("local", None, HomeType.LOCAL),
        ("hdd", None, HomeType.HDD),
        ("google", None, HomeType.GOOGLE),
        ("test", Path("test"), HomeType.TEST),
    ],
)
def test_home_path_from_settings(home_config, home_type_str, path, expected_type):
    home = Home.from_settings(home_type_str, home_config, path)
    assert home._type == expected_type
    assert home.home_path == Path(home_config[home_type_str]) if path is None else path
