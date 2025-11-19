from pathlib import Path
import datetime
import numpy as np
from pydantic import BaseModel, DirectoryPath, FilePath, computed_field

import susi.io.utils as io_utils


project_root_path = io_utils.get_project_root()


class FilePaths(BaseModel, strict=True):
    input_folder: DirectoryPath = project_root_path / Path("inputs/")
    output_folder: DirectoryPath = project_root_path / Path("outputs/")

    weather_data_path: FilePath = project_root_path / Path("inputs/CFw.csv")


class SimulationParameters(
    BaseModel,
    strict=True,
    frozen=True,
    arbitrary_types_allowed=True,  # This allows numpy arrays and other types which do not have built-in validation in Pydantic
):
    # Time
    start_date: datetime.datetime  # Start date for simulation
    end_date: datetime.datetime  # End day for simulation

    # Hydro
    strip_width_metres: float  # Distance between ditches

    # Forest
    # Age of different forest layers at the beginning of the simulation
    initial_dominant_stand_age_years: float
    initial_subdominant_stand_age_years: float
    initial_understorey_age_years: float
    site_fertility_class: int

    @computed_field
    @property
    def n_computation_nodes_in_strip(self) -> int:
        # Number of computation nodes in the strip, 2-m width of node
        return int(self.strip_width_metres / 2)

    @computed_field
    @property
    def ageSim(self) -> dict[str, np.ndarray]:
        # Age of stand for all nodes along the strip
        return {
            "dominant": self.initial_dominant_stand_age_years
            * np.ones(self.n_computation_nodes_in_strip),
            "subdominant": self.initial_subdominant_stand_age_years
            * np.ones(self.n_computation_nodes_in_strip),
            "under": self.initial_understorey_age_years
            * np.ones(self.n_computation_nodes_in_strip),
        }

    @computed_field
    @property
    def sfc(self) -> np.ndarray:
        # site fertility class for all nodes along the strip
        return (
            np.ones(self.n_computation_nodes_in_strip, dtype=int)
            * self.site_fertility_class
        )


class Config(BaseModel, strict=True):
    paths: FilePaths
    simulation_parameters: SimulationParameters
