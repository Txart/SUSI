from pathlib import Path
import datetime
import numpy as np
from typing import Annotated, Any, Dict, Type
from pydantic import (
    BaseModel,
    DirectoryPath,
    FilePath,
    computed_field,
    Field,
    ConfigDict,
)

import susi.io.utils as io_utils


project_root_path = io_utils.get_project_root()

PositiveFloat = Annotated[float, Field(gt=0)]
NonNegativeFloat = Annotated[float, Field(ge=0)]


class StrictFrozenModel(BaseModel):
    """
    Defines a stricter Pydantic class
    """

    model_config = ConfigDict(
        validate_assignment=True,  # validates on assignment
        frozen=True,  # immutable
        extra="forbid",  # forbid extra fields
        validate_default=True,  # validate default values
    )


class FilePaths(StrictFrozenModel):
    input_folder: DirectoryPath = project_root_path / Path("inputs/")
    output_folder: DirectoryPath = project_root_path / Path("outputs/")

    weather_data_path: FilePath = project_root_path / Path("inputs/CFw.csv")


class OrganicLayerParameters(StrictFrozenModel):
    org_depth: PositiveFloat = 0.04  # depth of organic top layer (m)
    org_poros: PositiveFloat = 0.9  # porosity (-)
    org_fc: PositiveFloat = 0.3  # field capacity (-)
    # critical vol. moisture content (-) for decreasing phase in Ef
    org_rw: PositiveFloat = 0.24
    pond_storage_max: PositiveFloat = 0.01  # max ponding allowed (m)

    # initial values
    org_sat: PositiveFloat = 1.0  # organic top layer saturation ratio (-)
    pond_storage: NonNegativeFloat = 0.0  # pond storage


class OrganicLayerParametersArray:
    """
    Same class as OrganicLayerParameters, but with all fields a numpy array of given length.
    """

    org_depth: np.ndarray
    org_poros: np.ndarray
    org_fc: np.ndarray
    org_rw: np.ndarray
    pond_storage_max: np.ndarray
    org_sat: np.ndarray
    pond_storage: np.ndarray

    def __init__(
        self, organic_layer_parameters: OrganicLayerParameters, array_length: int
    ):
        for name, value in organic_layer_parameters.model_dump().items():
            setattr(self, name, value * np.ones(array_length))


class WeatherParameters(StrictFrozenModel):
    infolder: DirectoryPath = project_root_path / "\\wfiles\\"
    infile_d: FilePath = Path("Tammela_weather_1.csv")
    start_yr: int = 1980
    end_yr: int = 1984
    description: str = "Undefined, Finland"
    lat: float = 65.00
    lon: float = 25.00


class CanopyStateParameters(StrictFrozenModel):
    lai_conif: float = 3.0  # conifer 1-sided LAI (m2 m-2)
    lai_decid_max: float = 0.01  # maximum annual deciduous 1-sided LAI (m2 m-2):
    hc: float = 16.0  # canopy height (m)
    cf: float = 0.7  # canopy closure fraction (-)
    # initial state of canopy storage [mm] and snow water equivalent [mm]
    w: float = 0.0  # canopy storage mm
    swe: float = 0.0  # snow water equivalent mm


class CanopyStateParametersArray:
    lai_conif: np.ndarray
    lai_decid_max: np.ndarray
    hc: np.ndarray
    cf: np.ndarray
    # initial state of canopy storage [mm] and snow water equivalent [mm]
    w: np.ndarray
    swe: np.ndarray

    def __init__(
        self, canopy_state_parameters: CanopyStateParameters, array_length: int
    ):
        for name, value in canopy_state_parameters.model_dump().items():
            setattr(self, name, value * np.ones(array_length))


class CanopyParameters(BaseModel):
    dt: float = 86400.0  # canopy model timestep

    class Flow(StrictFrozenModel):
        # Flow field
        zmeas: float = 2.0
        zground: float = 0.5
        zo_ground: float = 0.01

    class Interception(StrictFrozenModel):
        # interception
        wmax: float = 0.5
        wmaxsnow: float = 4.0

    class Snow(StrictFrozenModel):
        # degree-day snow model
        kmelt: float = 2.8934e-05  # melt coefficient in open (mm/s
        kfreeze: float = 5.79e-6  # freezing coefficient (mm/s)
        r: float = 0.05  # maximum fraction of liquid in snow (-)

    class Physpara(BaseModel):
        # canopy conductance
        amax: float = Field(
            frozen=False, default=10.0
        )  # maximum photosynthetic rate (umolm-2(leaf)s-1)
        g1_conif: float = 2.1  # stomatal parameter, conifers
        g1_decid: float = 3.5  # stomatal parameter, deciduous
        q50: float = 50.0  # light response parameter (Wm-2)
        kp: float = 0.6  # light attenuation parameter (-)
        rw: float = 0.20  # critical value for REW (-),
        rwmin: float = 0.02  # minimum relative conductance (-)
        # soil evaporation
        gsoil: float = 1e-2  # soil surface conductance if soil is fully wet (m/s)

    class Phenology(StrictFrozenModel):
        # seasonal cycle of physiology: smax [degC], tau[d], xo[degC],fmin[-](residual photocapasity)
        smax: float = 18.5  # degC
        tau: float = 13.0  # days
        xo: float = -4.0  # degC
        fmin: float = 0.05  # minimum photosynthetic capacity in winter (-)

    flow: Flow = Flow()
    interception: Interception = Interception()
    snow: Snow = Snow()
    physpara: Physpara = Physpara()
    phenology: Phenology = Phenology()
    state: CanopyStateParameters = CanopyStateParameters()


class SimulationParameters(
    StrictFrozenModel,
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


class Config(StrictFrozenModel):
    paths: FilePaths
    simulation_parameters: SimulationParameters


def get_susi_para(
    wlocation=None,
    peat=None,
    photosite="All data",
    folderName=None,
    hdomSim=None,
    volSim=None,
    ageSim=None,
    sarkaSim=None,
    sfc=None,
    susiPath=None,
    ddwest=None,
    ddeast=None,
    n=None,
    bd=None,
    peatN=None,
    peatP=None,
    peatK=None,
):
    # ********** Stand parameters and weather forcing*******************
    # --------------Weather variables 10 km x 10 km grid
    if susiPath is None:
        susiPath = ""
    wpara = {
        "undefined": {
            "infolder": susiPath + "\\wfiles\\",
            "infile_d": "Tammela_weather_1.csv",
            "start_yr": 1980,
            "end_yr": 1984,
            "description": "Undefined, Finland",
            "lat": 65.00,
            "lon": 25.00,
        },
    }

    cpara = CanopyParameters()
    org_para = OrganicLayerParameters()

    # Hannun parametrit
    # ------------ Soil and stand parameters ----------------------------------
    spara = {
        "develop_scens": {
            "sitename": "susirun",
            "species": "Pine",
            "sfc": sfc,
            "sfc_specification": 1,
            "hdom": hdomSim,
            "vol": volSim,
            "age": ageSim,
            "smc": "Peatland",
            "nLyrs": 60,
            "dzLyr": 0.05,
            "L": sarkaSim,
            "n": n,
            "ditch depth west": [
                -0.3,
                -0.6,
                -0.9,
            ],  # nLyrs kerrosten lkm, dzLyr kerroksen paksuus m, saran levys m, n laskentasolmulen lukumäärä, ditch depth pjan syvyys simuloinnin alussa m
            "ditch depth east": [-0.3, -0.6, -0.9],
            "ditch depth 20y west": [
                -0.3,
                -0.6,
                -0.9,
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "ditch depth 20y east": [
                -0.3,
                -0.6,
                -0.9,
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "scenario name": ["D30", "D60", "D90"],  # kasvunlisaykset
            "drain_age": 50,
            "initial h": -0.2,
            "slope": 0.0,
            "peat type": ["A", "A", "A", "A", "A", "A", "A", "A"],
            "peat type bottom": ["A"],
            "anisotropy": 10.0,
            "vonP": True,
            "vonP top": [2, 2, 2, 3, 4, 5, 6, 6],
            "vonP bottom": 8,
            "bd top": None,
            "bd bottom": 0.16,
            "peatN": peatN,
            "peatP": peatP,
            "peatK": peatK,
            "enable_peattop": True,
            "enable_peatmiddle": True,
            "enable_peatbottom": True,
            "h_mor": 0.03,  # depth of mor layer, m
            "rho_mor": 80.0,  # bulk density of mor layer, kg m-3
            "cutting_yr": 2058,  # year for cutting
            "cutting_to_ba": 12,  # basal area after cutting, m2/ha
            "depoN": 4.0,
            "depoP": 0.1,
            "depoK": 1.0,
            "fertilization": {
                "application year": 2201,
                "N": {
                    "dose": 0.0,
                    "decay_k": 0.5,
                    "eff": 1.0,
                },  # fertilization dose in kg ha-1, decay_k in yr-1
                "P": {"dose": 45.0, "decay_k": 0.2, "eff": 1.0},
                "K": {"dose": 100.0, "decay_k": 0.3, "eff": 1.0},
                "pH_increment": 1.0,
            },
            "canopylayers": {
                "dominant": np.ones((int(n)), dtype=int),
                "subdominant": np.zeros((int(n)), dtype=int),
                "under": np.zeros((int(n)), dtype=int),
            },
        },
        "wbal_scens": {
            "sitename": "susirun",
            "species": "Pine",
            "sfc": sfc,
            "sfc_specification": 1,
            "hdom": hdomSim,
            "vol": volSim,
            "age": ageSim,
            "smc": "Peatland",
            "nLyrs": 50,
            "dzLyr": 0.05,
            "L": sarkaSim,
            "n": n,
            "ditch depth west": [
                -0.5
            ],  # nLyrs kerrosten lkm, dzLyr kerroksen paksuus m, saran levys m, n laskentasolmulen lukumäärä, ditch depth pjan syvyys simuloinnin alussa m
            "ditch depth east": [-0.5],
            "ditch depth 20y west": [
                -0.5
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "ditch depth 20y east": [
                -0.5
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "scenario name": ["Wbalance"],  # kasvunlisaykset
            "initial h": -0.2,
            "slope": 0.0,
            "peat type": ["A", "A", "A", "A", "A", "A", "A", "A"],
            "peat type bottom": ["A"],
            "anisotropy": 10.0,
            "vonP": True,
            "vonP top": [2, 2, 2, 3, 4, 5, 6, 6],
            "vonP bottom": 8,
            "bd top": [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12],
            "bd bottom": 0.16,
            "peatN": peatN,
            "peatP": peatP,
            "peatK": peatK,
            "enable_peattop": True,
            "enable_peatmiddle": True,
            "enable_peatbottom": True,
            "h_mor": 0.01,  # depth of mor layer, m
            "rho_mor": 80.0,  # bulk density of mor layer, kg m-3
            "cutting_yr": 2058,  # year for cutting
            "cutting_to_ba": 12,  # basal area after cutting, m2/ha
            "depoN": 4.0,
            "depoP": 0.1,
            "depoK": 1.0,
            "fertilization": {
                "application year": 2201,
                "N": {
                    "dose": 0.0,
                    "decay_k": 0.5,
                    "eff": 1.0,
                },  # fertilization dose in kg ha-1, decay_k in yr-1
                "P": {"dose": 45.0, "decay_k": 0.075, "eff": 1.0},
                "K": {"dose": 100.0, "decay_k": 0.075, "eff": 1.0},
                "pH_increment": 1.0,
            },
            "canopylayers": {
                "dominant": np.ones((int(n)), dtype=int),
                "subdominant": np.zeros((int(n)), dtype=int),
                "under": np.zeros((int(n)), dtype=int),
            },
        },
        "krycklan": {
            "sitename": "susirun",
            "species": "Spruce",
            "sfc": sfc,
            "sfc_specification": 1,
            "hdom": hdomSim,
            "vol": volSim,
            "age": ageSim,
            "smc": "Peatland",
            "nLyrs": 30,
            "dzLyr": 0.05,
            "L": sarkaSim,
            "n": n,
            "ditch depth west": [
                -0.3,
                -0.6,
                -0.9,
            ],  # nLyrs kerrosten lkm, dzLyr kerroksen paksuus m, saran levys m, n laskentasolmulen lukumäärä, ditch depth pjan syvyys simuloinnin alussa m
            "ditch depth east": [-0.3, -0, 6, -0.9],
            "ditch depth 20y west": [
                -0.3,
                -0.6,
                -0.9,
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "ditch depth 20y east": [
                -0.3,
                -0.6,
                -0.9,
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "scenario name": ["D30", "D60", "D90"],  # kasvunlisaykset
            "initial h": -0.2,
            "slope": 3.0,
            "peat type": ["A", "A", "A", "A", "A", "A", "A", "A"],
            "peat type bottom": ["A"],
            "anisotropy": 50.0,
            "vonP": False,
            "vonP top": [2, 2, 2, 2, 4, 5, 5, 5],
            "vonP bottom": 5,
            "bd top": None,
            "bd bottom": 0.16,
            "peatN": 1.2,
            "peatP": 0.12,
            "peatK": 0.07,  # peat nutrient contents in gravimetric %
            "enable_peattop": True,
            "enable_peatmiddle": False,
            "enable_peatbottom": False,
            "h_mor": 0.04,  # depth of mor layer, m
            "rho_mor": 100.0,  # bulk density of mor layer, kg m-3
            "cutting_yr": 2058,  # year for cutting
            "cutting_to_ba": 12,  # basal area after cutting, m2/ha
            "depoN": 4.0,
            "depoP": 0.1,
            "depoK": 1.0,
            "fertilization": {
                "application year": 2201,
                "N": {
                    "dose": 0.0,
                    "decay_k": 0.5,
                    "eff": 1.0,
                },  # fertilization dose in kg ha-1, decay_k in yr-1
                "P": {"dose": 45.0, "decay_k": 0.2, "eff": 1.0},
                "K": {"dose": 100.0, "decay_k": 0.3, "eff": 1.0},
                "pH_increment": 1.0,
            },
            "canopylayers": {
                "dominant": np.ones((int(n)), dtype=int),
                "subdominant": np.zeros((int(n)), dtype=int),
                "under": np.zeros((int(n)), dtype=int),
            },
        },
        "ullika": {
            "sitename": "susirun",
            "species": "Pile",
            "sfc": sfc,
            "sfc_specification": 1,
            "hdom": hdomSim,
            "vol": volSim,
            "age": ageSim,
            "smc": "Peatland",
            "nLyrs": 30,
            "dzLyr": 0.05,
            "L": sarkaSim,
            "n": n,
            "ditch depth west": [
                -0.3,
                -0.6,
                -0.9,
            ],  # nLyrs kerrosten lkm, dzLyr kerroksen paksuus m, saran levys m, n laskentasolmulen lukumäärä, ditch depth pjan syvyys simuloinnin alussa m
            "ditch depth east": [-0.1, -0.3, -0.9],
            "ditch depth 20y west": [
                -0.3,
                -0.6,
                -0.9,
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "ditch depth 20y east": [
                -0.1,
                -0.3,
                -0.9,
            ],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
            "scenario name": ["D30", "D60", "D90"],  # kasvunlisaykset
            "initial h": -0.2,
            "slope": 0.5,
            "peat type": ["A", "A", "A", "A", "A", "S", "S", "S"],
            "peat type bottom": ["S"],
            "anisotropy": 10.0,
            "vonP": False,
            "vonP top": [2, 2, 2, 2, 4, 5, 5, 5],
            "vonP bottom": 7,
            "bd top": None,
            "bd bottom": 0.16,
            "peatN": 0.86,
            "peatP": 0.007,
            "peatK": 0.026,  # peat nutrient contents in gravimetric %
            "enable_peattop": True,
            "enable_peatmiddle": True,
            "enable_peatbottom": True,
            "h_mor": 0.04,  # depth of mor layer, m
            "rho_mor": 100.0,  # bulk density of mor layer, kg m-3
            "cutting_yr": 2058,  # year for cutting
            "cutting_to_ba": 12,  # basal area after cutting, m2/ha
            "depoN": 4.0,
            "depoP": 0.1,
            "depoK": 1.0,
            "fertilization": {
                "application year": 2201,
                "N": {
                    "dose": 0.0,
                    "decay_k": 0.5,
                    "eff": 1.0,
                },  # fertilization dose in kg ha-1, decay_k in yr-1
                "P": {"dose": 45.0, "decay_k": 0.2, "eff": 1.0},
                "K": {"dose": 100.0, "decay_k": 0.3, "eff": 1.0},
                "pH_increment": 1.0,
            },
            "canopylayers": {
                "dominant": np.ones((int(n)), dtype=int),
                "subdominant": np.zeros((int(n)), dtype=int),
                "under": np.zeros((int(n)), dtype=int),
            },
        },
    }
    # ------------  Output parameters -------------------------------------------------
    outpara = {
        "outfolder": folderName,
        "netcdf": "susi.nc",
        #'netcdf': 'susi_ba18.nc',
        #'netcdf': 'susi_strip.nc',
        #'netcdf': 'susi_cc.nc',
        "startday": 1,
        "startmonth": 7,  # Päivä, josta keskiarvojen laskenta alkaa
        "endday": 31,
        "endmonth": 8,  # Päivä, johon keskiarvojen laskenta loppuu
        #'figs': True, 'to_file':True, 'static stand':False, 'hydfig':True, 'DOCfig':False,
    }
    photopara = {
        "All data": {
            "beta": 0.513,
            "gamma": 0.0196,
            "kappa": -0.389,
            "tau": 7.2,
            "X0": -4.0,
            "Smax": 17.3,
            "alfa": 1.0,
            "nu": 5.0,
        },
        "Sodankyla": {
            "beta": 0.831,
            "gamma": 0.065,
            "kappa": -0.150,
            "tau": 10.2,
            "X0": -0.9,
            "Smax": 16.4,
            "alfa": 1.0,
            "nu": 5.0,
        },
        "Hyytiala": {
            "beta": 0.504,
            "gamma": 0.0303,
            "kappa": -0.235,
            "tau": 11.1,
            "X0": -3.1,
            "Smax": 17.3,
            "alfa": 1.0,
            "nu": 5.0,
        },
        "Norunda": {
            "beta": 0.500,
            "gamma": 0.0220,
            "kappa": -0.391,
            "tau": 5.7,
            "X0": -4.0,
            "Smax": 17.6,
            "alfa": 1.062,
            "nu": 11.27,
        },
        "Tharandt": {
            "beta": 0.742,
            "gamma": 0.0267,
            "kappa": -0.512,
            "tau": 1.8,
            "X0": -5.2,
            "Smax": 18.5,
            "alfa": 1.002,
            "nu": 442.0,
        },
        "Bray": {
            "beta": 0.459,
            "gamma": -0.000669,
            "kappa": -0.560,
            "tau": 2.6,
            "X0": -17.6,
            "Smax": 45.0,
            "alfa": 0.843,
            "nu": 2.756,
        },
    }
    # ----------- Arrange and make coherent------
    # cpara['lat']=wpara[wlocation]['lat']; cpara['lon']=wpara[wlocation]['lon']

    o_w = wpara[wlocation] if wlocation is not None else wpara
    o_s = spara[peat] if peat is not None else spara
    o_p = photopara[photosite] if photosite is not None else photopara

    return o_w, cpara, org_para, o_s, outpara, o_p
