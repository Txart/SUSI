# -*- coding: utf-8 -*-
"""
Created on 17 Nov 2025

@author: alauren, txart
"""

import susi.io.utils as io_utils
from susi.core.susi_main import Susi
from susi.core.susi_utils import read_FMI_weather
from susi.io.app_structure import AppStructure
from susi.io.metadata_model import MetaData
from susi.io.parameters import golden_test

# ***************** local call for SUSI*****************************************************

metadata = MetaData()
app_structure = AppStructure()

# mottifile, dict of dicts, telling the growth and yield (Motti files) in each canopy layer with key pointing to integer in the canopylayer dict
mottifile = {
    "path": str(app_structure.input_folder) + "/",  # Input file folder
    "dominant": {1: "CF_41.xlsx"},  # Motti-file for the dominant layer
    "subdominant": {
        0: "susi_motti_input_lyr_1.xlsx"
    },  # subdominant layer Mottifle, 0 if not in use
    "under": {0: "susi_motti_input_lyr_2.xlsx"},
}  # understorey layer Mottifile, 0 if not in use


wpara = {
    "undefined": {
        "infolder": "" + "\\wfiles\\",
        "infile_d": "Tammela_weather_1.csv",
        "start_yr": 1980,
        "end_yr": 1984,
        "description": "Undefined, Finland",
        "lat": 65.00,
        "lon": 25.00,
    },
}
wpara = wpara["undefined"]


susi = Susi()  # Initaiate susi class

forc = read_FMI_weather(
    0,
    golden_test.PARAMETERS.simulation_parameters.start_date,
    golden_test.PARAMETERS.simulation_parameters.end_date,
    sourcefile=metadata.weather_data_path,
)  # read weather input

cpara = golden_test.PARAMETERS.canopy_parameters
org_para = golden_test.PARAMETERS.organic_layer_parameters
spara = golden_test.PARAMETERS.simulation_parameters
photopara = golden_test.PARAMETERS.photo_parameters
outpara = golden_test.PARAMETERS.output_parameters

# Create output folder
io_utils.create_folder(path=metadata.experiment_folder_path)

# Write output parameters
golden_test.PARAMETERS.dump_json_to_file(
    experiments_folder=metadata.experiment_folder_path
)
metadata.dump_json_to_file()

susi.run_susi(
    forc,
    wpara,
    cpara,
    org_para,
    spara,
    outpara,
    photopara,
    start_yr=golden_test.PARAMETERS.simulation_parameters.start_date.year,
    end_yr=golden_test.PARAMETERS.simulation_parameters.end_date.year,
    wlocation="undefined",
    mottifile=mottifile,
    peat="other",
    photosite="All data",
    folderName=str(app_structure.output_folder) + "/",
    ageSim=golden_test.PARAMETERS.simulation_parameters.age,
    sarkaSim=golden_test.PARAMETERS.simulation_parameters.L,
    sfc=golden_test.PARAMETERS.simulation_parameters.sfc,
)  # Run susi
