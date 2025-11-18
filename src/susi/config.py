from dataclasses import dataclass
from pathlib import Path

import susi.io.utils as io_utils


@dataclass
class FilePaths:
    input_folder: Path
    output_folder: Path

    weather_data_path: Path

    def __post_init__(self):
        for path in (self.input_folder, self.output_folder, self.weather_data_path):
            if not path.exists:
                raise FileNotFoundError(f"File or folder {path} could not be found.")


@dataclass
class Config:
    paths: FilePaths


project_root_path = io_utils.get_project_root()

CONFIG = Config(
    FilePaths(
        input_folder=project_root_path / Path("inputs/"),
        output_folder=project_root_path / Path("outputs/"),
        weather_data_path=project_root_path / Path("inputs/CFw.csv"),
    )
)
