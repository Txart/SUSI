# Checks whether the results of executing susi_calls.py
# change over time or not.
# Useful to know if my changes are changing the code in any way.

# PROCEDURE
# the True or Golden results of calling susi_calls.py are stored in golden_susi.nc
# We compute the sha256 hash of that file.
# Then we call the modified susi_calls.py, store it in susi.nc, and compute the sha256 hash.
# The hashes of the 2 files should be identical.


import hashlib
import subprocess
from pathlib import Path

import netCDF4
import numpy as np

from susi.io import netcdf_utils
from susi.io.app_structure import AppStructure
from susi.io.utils import get_project_root


def hash_netcdf_file(file_path, variables=None):
    """
    Compute SHA-256 hash of numerical data in a NetCDF4 file.

    Args:
        file_path (str): path to NetCDF4 file
        variables (list or None): list of variable names to include.
                                  If None, all variables are included.

    Returns:
        str: hex digest of SHA-256 hash
    """
    ds = netCDF4.Dataset(file_path, "r")

    # Read all datasets
    all_var_paths = netcdf_utils.list_variable_absolute_paths(group=ds)
    all_data = {
        var_path: netcdf_utils.get_var_by_path(ds, var_path)
        for var_path in all_var_paths
    }

    h = hashlib.sha256()

    data_bytes = np.ascontiguousarray(all_data).tobytes()
    h.update(data_bytes)

    ds.close()
    return h.hexdigest()


project_root_path = get_project_root()

app_structure = AppStructure()

CURRENT_SUSI_CALLS_PATH = project_root_path / Path("tools/susi_calls.py")
GOLDEN_NETCDF_FILE_PATH = project_root_path / Path("golden_file_test/golden_susi.nc")
NEW_SUSI_NETCDF_FILE_PATH = app_structure.output_folder / Path("susi.nc")

print("Computing golden hash...")
golden_hash = hash_netcdf_file(file_path=GOLDEN_NETCDF_FILE_PATH)
print(f"Golden hash = {golden_hash}")

print("Executing susi_calls.py...")
subprocess.run(
    ["python", str(CURRENT_SUSI_CALLS_PATH)],
    check=True,
)

print("Computing susi.nc hash...")
current_hash = hash_netcdf_file(file_path=NEW_SUSI_NETCDF_FILE_PATH)
print(f"Current hash = {current_hash}")

test_passes = golden_hash == current_hash

if not test_passes:
    raise ValueError("ERROR in the golden test!")
else:
    print("---------------------")
    print("Golden test passed!")
    print("---------------------")
