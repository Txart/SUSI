from pathlib import Path
from typing import Self
from pydantic import (
    BaseModel,
    DirectoryPath,
    FilePath,
    ConfigDict,
    Field,
    model_validator,
)

import susi.io.utils as io_utils


project_root_path = io_utils.get_project_root()


class MetaData(BaseModel):
    model_config = ConfigDict(
        validate_default=True,  # validate default values
    )

    metadata_schema_version: int = 1

    input_folder: DirectoryPath = project_root_path / Path("inputs/")
    parent_output_folder: DirectoryPath = project_root_path / Path("outputs/")

    weather_data_path: FilePath = project_root_path / Path("inputs/CFw.csv")

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

    experiment_folder_path: Path = Field(
        init=False,
        default=Path(),
        description="Where all simulation results go. The name of the folder is the experiment_id.",
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
        self.experiment_folder_path = self.parent_output_folder.joinpath(experiment_id)

        return self

    @model_validator(mode="after")
    def create_experiment_folder(self):
        # Creates experiment folder after validation

        io_utils.create_folder(path=self.experiment_folder_path)
        return self
