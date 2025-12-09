from pathlib import Path
import netCDF4
import pandas as pd

import susi.io.utils as io_utils
from susi.io import netcdf_utils
from susi.io.app_structure import AppStructure

app_structure = AppStructure()


def list_subdirectories(path: Path):
    return (x for x in path.iterdir() if x.is_dir())


def _load_single_experiment_metadatas(experiment_folderpath: Path) -> pd.DataFrame:
    """
    Reads metadata and parameter info from json files.
    Returns dict of all json values.
    """
    metadata_filepath = experiment_folderpath / app_structure.metadata_store_filename
    params_filepath = experiment_folderpath / app_structure.parameter_store_filename

    metadata, params = map(
        io_utils.read_json_file, [metadata_filepath, params_filepath]
    )
    return pd.json_normalize(metadata | params)


def coerce_datetime_format(df: pd.DataFrame) -> pd.DataFrame:
    datetime_cols = ["timestamp_start", "timestamp_end"]
    for col in datetime_cols:
        df[col] = pd.to_datetime(df[col], format=io_utils.datetime_format())
    return df


def modify_after_load(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # set datetime formats
    df = coerce_datetime_format(df)

    # sort by starting date first
    df = df.sort_values(by="timestamp_start", ignore_index=True, ascending=False)

    return df


def load_all_metadatas() -> pd.DataFrame:
    experiment_folderpaths = list_subdirectories(app_structure.output_folder)
    df = pd.concat(
        [
            _load_single_experiment_metadatas(exp_fpath)
            for exp_fpath in experiment_folderpaths
        ]
    )

    return modify_after_load(df)


df = load_all_metadatas()

# Query and filer and stuff...
df[df["photo_parameters.alfa"] > 0]

# Then make some functions to pass the filtered df and get the (lazy loaded) netcdf data.

# %% Read ncdf data
ds = netCDF4.Dataset(app_structure.output_folder / Path("susi.nc"), "r")
ds.groups


# Read all datasets
all_var_paths = netcdf_utils.list_variable_absolute_paths(group=ds)
all_data = {
    var_path: netcdf_utils.get_var_by_path(ds, var_path) for var_path in all_var_paths
}


# ds.close()
