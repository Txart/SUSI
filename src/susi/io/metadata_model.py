import platform
from importlib.metadata import version
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, FilePath, model_validator

import susi.io.utils as io_utils
from susi.io.app_structure import AppStructure

app_structure = AppStructure()


class MetaData(BaseModel):
    model_config = ConfigDict(
        validate_default=True,  # validate default values
    )

    metadata_schema_version: int = 1

    weather_data_path: FilePath = io_utils.get_project_root() / Path("inputs/CFw.csv")

    experiment_folder_path: Path = Field(
        init=False,
        default=Path(),
        description="Where all simulation results go. The name of the folder is the experiment_id.",
    )

    experiment_id: str = Field(
        init=False,
        default=str(),
        description="Uniquely identifies each simulation experiment. Format <date_time_random-integer>.",
    )

    timestamp_start: str = Field(
        init=False,
        default=str(),
        description="Initial timestamp. (Technically, it takes the timestamp at the time the current class is created).",
    )

    timestamp_end: str = Field(
        init=False,
        default=str(),
        description="Final timestamp, recorded when the metadata dumping is done.",
    )

    git_commit: str = Field(
        init=False,
        default=io_utils.get_git_revision_short_hash(),
        description="Git commit identifier.",
    )

    susi_version: str = Field(
        init=False,
        default=version("susi"),
        description="Model version as it appears in pyproject.toml",
    )

    host_info: str = Field(
        init=False,
        default=str(platform.uname()),
        description="Info about who ran the simulations.",
    )

    @model_validator(mode="after")
    def set_variables_with_current_timestamp(self):
        # Compute current timestamp and experiment_id once
        current_timestamp = io_utils.generate_current_datetime_stamp()
        experiment_id = io_utils.generate_experiment_ID(
            datetime_stamp=current_timestamp
        )

        self.timestamp_start = current_timestamp
        self.experiment_id = experiment_id
        self.experiment_folder_path = app_structure.output_folder.joinpath(
            experiment_id
        )

        return self

    def dump_json_to_file(self) -> None:
        filepath = self.experiment_folder_path / app_structure.metadata_store_filename
        with open(filepath, "w") as f:
            f.write(self.model_dump_json())
