from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class HomeType(Enum):
    LOCAL = "local"
    HDD = "hdd"
    GOOGLE = "google"
    TEST = "test"


@dataclass(frozen=True)
class Home:
    _type: HomeType
    _type_to_path: dict[HomeType, Path]

    @classmethod
    def from_settings(cls, home_type: str, path: Path | None = None) -> Home:
        _type_to_path = {
            HomeType.LOCAL: Path("/Users/alexis/tabs"),
            HomeType.HDD: Path("/Volumes/Elements/tabs"),
            HomeType.GOOGLE: Path("/mnt/disks/tabs"),
        }
        home_type_object = HomeType(home_type)
        if home_type_object is HomeType.TEST:
            assert path is not None
            _type_to_path[home_type_object] = path
        else:
            assert path is None

        return cls(home_type_object, _type_to_path)

    @property
    def home_path(self) -> Path:
        return self._type_to_path[self._type]
