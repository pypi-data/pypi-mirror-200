from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class HomeType(Enum):
    LOCAL = "local"
    HDD = "hdd"
    BUCKET = "bucket"
    GOOGLE = "google"
    TEST = "test"


@dataclass(frozen=True)
class Home:
    _type: HomeType
    _type_to_path: dict[HomeType, Path]

    @classmethod
    def from_settings(
        cls, home_type: str, home_config: dict, path: Path | None = None
    ) -> Home:
        """
        home_config is a dict of the form:
        home:
            local: /Users/alexis/tabs
            hdd: /Volumes/Elements/tabs
            bucket: /mnt/disks/tabs
            google: /home/alexis
        """
        if path is None:
            path = Path(home_config[home_type])
        return cls(HomeType(home_type), {HomeType(home_type): path})

    @property
    def home_path(self) -> Path:
        return self._type_to_path[self._type]
