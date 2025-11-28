from pydantic import (
    BaseModel,
    DirectoryPath,
)
from pathlib import Path

import susi.io.utils as io_utils


class AppStructure(BaseModel):
    project_root_path: DirectoryPath = io_utils.get_project_root()
    input_folder: DirectoryPath = project_root_path / Path("inputs/")
    output_folder: DirectoryPath = project_root_path / Path("outputs/")

    metadata_store_filename: str = "metadata.json"
    parameter_store_filename: str = "params.json"
