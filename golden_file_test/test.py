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

from susi.config import CONFIG
from susi.io.utils import get_project_root


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


project_root_path = get_project_root()

CURRENT_SUSI_CALLS_PATH = project_root_path / Path("simulations/susi_calls.py")
GOLDEN_NETCDF_FILE_PATH = project_root_path / Path("golden_file_test/golden_susi.nc")
NEW_SUSI_NETCDF_FILE_PATH = CONFIG.paths.output_folder / Path("susi.nc")

print("Computing golden hash...")
golden_hash = sha256_file(GOLDEN_NETCDF_FILE_PATH)

print("Executing susi_calls.py and saving the outputs to golden_file_test/susi.nc...")
subprocess.run(
    ["python", str(CURRENT_SUSI_CALLS_PATH)],
    check=True,
)

print("Computing susi.nc hash...")
current_hash = sha256_file(GOLDEN_NETCDF_FILE_PATH)

test_passes = golden_hash == current_hash

if not test_passes:
    raise ValueError("ERROR in the golden test!")
else:
    print("---------------------")
    print("Golden test passed!")
    print("---------------------")
