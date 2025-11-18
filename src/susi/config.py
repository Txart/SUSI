from dataclasses import dataclass
from pathlib import Path
import datetime
import numpy as np

import susi.io.utils as io_utils


project_root_path = io_utils.get_project_root()


@dataclass
class FilePaths:
    input_folder: Path = project_root_path / Path("inputs/")
    output_folder: Path = project_root_path / Path("outputs/")

    weather_data_path: Path = project_root_path / Path("inputs/CFw.csv")

    def __post_init__(self):
        for path in (self.input_folder, self.output_folder, self.weather_data_path):
            if not path.exists:
                raise FileNotFoundError(f"File or folder {path} could not be found.")


@dataclass
class SimulationParameters:
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

    def __post_init__(self):
        # Number of computation nodes in the strip, 2-m width of node
        self.n_computation_nodes_in_strip = int(self.strip_width_metres / 2)

        # Age of stand for all nodes along the strip
        self.ageSim = {
            "dominant": self.initial_dominant_stand_age_years
            * np.ones(self.n_computation_nodes_in_strip),
            "subdominant": self.initial_subdominant_stand_age_years
            * np.ones(self.n_computation_nodes_in_strip),
            "under": self.initial_understorey_age_years
            * np.ones(self.n_computation_nodes_in_strip),
        }

        # site fertility class for all nodes along the strip
        self.sfc = (
            np.ones(self.n_computation_nodes_in_strip, dtype=int)
            * self.site_fertility_class
        )


@dataclass
class Config:
    paths: FilePaths
    simulation_parameters: SimulationParameters
