# Checks whether the results of executing susi_calls.py
# change over time or not.
# Useful to know if my changes are changing the code in any way.

# PROCEDURE
# the True or Golden results of calling susi_calls.py are stored in golden_susi.nc
# We compute the sha256 hash of that file.
# Then we call the modified susi_calls.py, store it in susi.nc, and compute the sha256 hash.
# The hashes of the 2 files should be identical.


from pathlib import Path
import hashlib
import subprocess
import netCDF4
import numpy as np

from susi.io.metadata_model import MetaData
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

    if variables is None:
        variables = list(ds.variables.keys())

    h = hashlib.sha256()

    for var in variables:
        data = ds.variables[var][:]
        # Ensure data is contiguous and in consistent byte order
        data_bytes = np.ascontiguousarray(data).tobytes()
        h.update(data_bytes)

    ds.close()
    return h.hexdigest()


project_root_path = get_project_root()

default_file_paths = MetaData()

CURRENT_SUSI_CALLS_PATH = project_root_path / Path("tools/susi_calls.py")
GOLDEN_NETCDF_FILE_PATH = project_root_path / Path("golden_file_test/golden_susi.nc")
NEW_SUSI_NETCDF_FILE_PATH = default_file_paths.parent_output_folder / Path("susi.nc")

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
