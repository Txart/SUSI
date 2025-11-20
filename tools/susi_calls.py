# -*- coding: utf-8 -*-
"""
Created on 17 Nov 2025

@author: alauren, txart
"""

import numpy as np
import datetime
from susi.core.susi_utils import read_FMI_weather
from susi.config import get_susi_para
from susi.core.susi_main import Susi
from susi.config import Config, FilePaths, SimulationParameters

# ***************** local call for SUSI*****************************************************

CONFIG = Config(
    paths=FilePaths(),
    simulation_parameters=SimulationParameters(
        start_date=datetime.datetime(2004, 1, 1),
        end_date=datetime.datetime(2005, 12, 31),
        strip_width_metres=40.0,
        initial_dominant_stand_age_years=100.0,
        initial_subdominant_stand_age_years=0.0,
        initial_understorey_age_years=0.0,
        site_fertility_class=4,
    ),
)

# mottifile, dict of dicts, telling the growth and yield (Motti files) in each canopy layer with key pointing to integer in the canopylayer dict
mottifile = {
    "path": str(CONFIG.paths.input_folder) + "/",  # Input file folder
    "dominant": {1: "CF_41.xlsx"},  # Motti-file for the dominant layer
    "subdominant": {
        0: "susi_motti_input_lyr_1.xlsx"
    },  # subdominant layer Mottifle, 0 if not in use
    "under": {0: "susi_motti_input_lyr_2.xlsx"},
}  # understorey layer Mottifile, 0 if not in use


site = "develop_scens"  # name of the parameter set in get_susi_para


wpara, cpara, org_para, spara, outpara, photopara = get_susi_para(
    wlocation="undefined",
    peat=site,
    folderName=str(CONFIG.paths.output_folder) + "/",
    hdomSim=None,
    ageSim=CONFIG.simulation_parameters.ageSim,
    sarkaSim=CONFIG.simulation_parameters.strip_width_metres,
    sfc=CONFIG.simulation_parameters.sfc,
    n=CONFIG.simulation_parameters.n_computation_nodes_in_strip,
)

spara["cutting_yr"] = (
    2001  # cutting year, not used if year is outside the simulation period
)
spara["drain_age"] = 100.0  # time since drainage, yrs
mass_mor = (
    1.616 * np.log(spara["drain_age"]) - 1.409
)  # Pitkänen et al. 2012 Forest Ecology and Management 284 (2012) 100–106

if np.median(CONFIG.simulation_parameters.sfc) > 4:
    spara["peat type"] = [
        "S",
        "S",
        "S",
        "S",
        "S",
        "S",
        "S",
        "S",
    ]  # Peat type 'S' if Sphagnum, 'A' if woody or Carex-peat
    spara["peat type bottom"] = ["A"]
    spara["vonP top"] = [2, 5, 5, 5, 6, 6, 7, 7]  # Degree of decomposition
    spara["anisotropy"] = 10  # Anisotropy of peat hydraulic conductivity
    spara["rho_mor"] = 80.0  # bulk density of mor layer kg m-3
else:
    spara["vonP top"] = [2, 5, 5, 5, 6, 6, 7, 7]
    spara["anisotropy"] = 10
    spara["rho_mor"] = 90.0

spara["h_mor"] = mass_mor / spara["rho_mor"]

spara["ditch depth west"] = [
    -0.5
]  # ditch depth at the beginning of simulation m, if given several values SUSI calculates scenarios for each ditch depth
spara["ditch depth east"] = [-0.5]
spara["ditch depth 20y west"] = [-0.5]  # Ditch depth after 20 yrs, m, negative down
spara["ditch depth 20y east"] = [-0.5]  # Ditch depth after 20 yrs, m, negative down
spara["scenario name"] = [
    "D60"
]  # Scanario names, equal nmber of names than ditch depth scenarios
# spara['enable_peatmiddle'] = False,
# spara['enable_peatbottom'] = False

susi = Susi()  # Initaiate susi class

forc = read_FMI_weather(
    0,
    CONFIG.simulation_parameters.start_date,
    CONFIG.simulation_parameters.end_date,
    sourcefile=CONFIG.paths.weather_data_path,
)  # read weather input

susi.run_susi(
    forc,
    wpara,
    cpara,
    org_para,
    spara,
    outpara,
    photopara,
    start_yr=CONFIG.simulation_parameters.start_date.year,
    end_yr=CONFIG.simulation_parameters.end_date.year,
    wlocation="undefined",
    mottifile=mottifile,
    peat="other",
    photosite="All data",
    folderName=str(CONFIG.paths.output_folder) + "/",
    ageSim=CONFIG.simulation_parameters.ageSim,
    sarkaSim=CONFIG.simulation_parameters.strip_width_metres,
    sfc=CONFIG.simulation_parameters.sfc,
)  # Run susi
