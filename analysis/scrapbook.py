from pathlib import Path
import netCDF4
import pandas as pd

from susi.io import netcdf_utils
from susi.io.app_structure import AppStructure
from susi.io.metadata_model import MetaData
from susi.io.parameter_model import Params
import susi.io.utils as io_utils
from susi.io import netcdf_utils

app_structure = AppStructure()


def list_subdirectories(path: Path):
    return (x for x in path.iterdir() if x.is_dir())


experiment_folderpaths = list_subdirectories(app_structure.output_folder)

experiment_folderpaths = list(experiment_folderpaths)
metadata_filepath = experiment_folderpaths[0] / app_structure.metadata_store_filename
params_filepath = experiment_folderpaths[0] / app_structure.parameter_store_filename


metadata = io_utils.read_json_file(path=metadata_filepath)
params = io_utils.read_json_file(path=params_filepath)

# Can put data back into original pydantic model if we need
# _ = MetaData.model_validate(metadata)
# _ = Params.model_validate(params)

all_data = metadata | params

df = pd.json_normalize([all_data])

# %% Read ncdf data
ds = netCDF4.Dataset(app_structure.output_folder / Path("susi.nc"), "r")
ds.groups


# Read all datasets
all_var_paths = netcdf_utils.list_variable_absolute_paths(group=ds)
all_data = {
    var_path: netcdf_utils.get_var_by_path(ds, var_path) for var_path in all_var_paths
}

ds.close()


# %%
ds = netCDF4.Dataset(app_structure.output_folder / Path("susi.nc"), "r")

# Read all datasets
all_var_paths = netcdf_utils.list_variable_absolute_paths(group=ds)
all_data = {
    var_path: netcdf_utils.get_var_by_path(ds, var_path) for var_path in all_var_paths
}

with open("susinc.txt", "w") as f:
    f.write(str(all_data))

ds.close()

ds = netCDF4.Dataset(
    app_structure.project_root_path / Path("golden_file_test/golden_susi.nc"), "r"
)

# Read all datasets
all_var_paths = netcdf_utils.list_variable_absolute_paths(group=ds)
all_data = {
    var_path: netcdf_utils.get_var_by_path(ds, var_path) for var_path in all_var_paths
}

with open("golden_susinc.txt", "w") as f:
    f.write(str(all_data))

ds.close()
