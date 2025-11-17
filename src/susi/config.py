from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    input_folder: Path
    output_folder: Path

    weather_data_path: Path


CONFIG = Config(
    input_folder=Path("inputs/"),
    output_folder=Path("outputs/"),
    weather_data_path=Path("inputs/CFw.csv"),
)
