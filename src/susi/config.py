from pathlib import Path
import datetime
import numpy as np
from typing import Annotated, Callable
from enum import Enum
from pydantic import (
    BaseModel,
    DirectoryPath,
    FilePath,
    computed_field,
    Field,
    ConfigDict,
    field_validator,
)

import susi.io.utils as io_utils


project_root_path = io_utils.get_project_root()

PositiveFloat = Annotated[float, Field(gt=0)]
NonNegativeFloat = Annotated[float, Field(ge=0)]
NonPositiveFloat = Annotated[float, Field(le=0)]


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


class MetaData(StrictFrozenModel):
    input_folder: DirectoryPath = project_root_path / Path("inputs/")
    parent_output_folder: DirectoryPath = project_root_path / Path("outputs/")

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


class OutputParameters(StrictFrozenModel):
    outfolder: DirectoryPath = project_root_path / Path("outputs/")
    netcdf: Path = Path("susi.nc")
    startday: int = 1
    startmonth: int = 7  # Päivä josta keskiarvojen laskenta alkaa
    endday: int = 31
    endmonth: int = 8  # Päivä johon keskiarvojen laskenta loppuu


class PhotoParameters(StrictFrozenModel):
    # photosynthesis parameters for assimilation model (Mäkelä et al. 2008)
    beta: float
    gamma: float
    kappa: float
    tau: float
    X0: float
    Smax: float
    alfa: float
    nu: float


class LocationsForPhotoParams(str, Enum):
    all_data = "All_data"
    sodankyla = "Sodankyla"
    hyytiala = "Hyytiala"
    norunda = "Norunda"
    tharandt = "Tharandt"
    bray = "Bray"


PRESET_PHOTO_PARAMETERS: dict[str, PhotoParameters] = {
    "All_data": PhotoParameters(
        beta=0.513,
        gamma=0.0196,
        kappa=-0.389,
        tau=7.2,
        X0=-4.0,
        Smax=17.3,
        alfa=1.0,
        nu=5.0,
    ),
    "Sodankyla": PhotoParameters(
        beta=0.831,
        gamma=0.065,
        kappa=-0.150,
        tau=10.2,
        X0=-0.9,
        Smax=16.4,
        alfa=1.0,
        nu=5.0,
    ),
    "Hyytiala": PhotoParameters(
        beta=0.504,
        gamma=0.0303,
        kappa=-0.235,
        tau=11.1,
        X0=-3.1,
        Smax=17.3,
        alfa=1.0,
        nu=5.0,
    ),
    "Norunda": PhotoParameters(
        beta=0.500,
        gamma=0.0220,
        kappa=-0.391,
        tau=5.7,
        X0=-4.0,
        Smax=17.6,
        alfa=1.062,
        nu=11.27,
    ),
    "Tharandt": PhotoParameters(
        beta=0.742,
        gamma=0.0267,
        kappa=-0.512,
        tau=1.8,
        X0=-5.2,
        Smax=18.5,
        alfa=1.002,
        nu=442.0,
    ),
    "Bray": PhotoParameters(
        beta=0.459,
        gamma=-0.000669,
        kappa=-0.560,
        tau=2.6,
        X0=-17.6,
        Smax=45.0,
        alfa=0.843,
        nu=2.756,
    ),
}


def get_photo_parameters_by_location(
    location: LocationsForPhotoParams,
) -> PhotoParameters:
    return PRESET_PHOTO_PARAMETERS[location.value]


class TreeSpecies(str, Enum):
    pine = "Pine"
    spruce = "Spruce"
    birch = "Birch"


class PeatTypes(str, Enum):
    all_types = "A"
    sphagnum = "S"
    carex = "C"
    wood = "L"


class NutrientFertilizationParameters(StrictFrozenModel):
    dose: NonNegativeFloat = Field(
        description="Dose of compound in fertilizer, kg ha-1"
    )
    decay_k: NonNegativeFloat = Field(description="Decay rate, yr-1")
    eff: NonNegativeFloat = Field(description="Nutrient use efficiency")


class FertilizationParameters(StrictFrozenModel):
    application_year: int = 2201
    N: NutrientFertilizationParameters
    P: NutrientFertilizationParameters
    K: NutrientFertilizationParameters
    pH_increment: NonNegativeFloat = 1.0


class SimulationParameters(
    StrictFrozenModel,
    arbitrary_types_allowed=True,  # This allows numpy arrays and other types which do not have built-in validation in Pydantic
):
    # Time
    start_date: datetime.datetime  # Start date for simulation
    end_date: datetime.datetime  # End day for simulation

    # Forest
    # Age of different forest layers at the beginning of the simulation
    initial_dominant_stand_age_years: float
    initial_subdominant_stand_age_years: float
    initial_understorey_age_years: float

    site_fertility_class: int
    sitename: str
    species: TreeSpecies
    sfc_specification: float
    hdom: float | None
    vol: float | None
    smc: str
    nLyrs: int
    dzLyr: float
    L: float = Field(description="Strip width, i.e., distance between ditches, m")
    ditch_depth_west: list[NonPositiveFloat] = Field(
        description="nLyrs kerrosten lkm, dzLyr kerroksen paksuus m, saran levys m, n laskentasolmulen lukumäärä, ditch depth pjan syvyys simuloinnin alussa m"
    )
    ditch_depth_east: list[NonPositiveFloat]
    ditch_depth_20y_west: list[NonPositiveFloat] = Field(
        description=" ojan syvyys 20 vuotta simuloinnin aloituksesta"
    )
    ditch_depth_20y_east: list[NonPositiveFloat] = Field(
        description="ojan syvyys 20 vuotta simuloinnin aloituksesta"
    )
    scenario_name: list[str] = Field(description=" kasvunlisaykset")
    drain_age: float
    initial_h: float
    slope: float
    peat_type: list[str]
    peat_type_bottom: list[str]
    anisotropy: float = Field(description="Anisotropy of peat hydraulic conductivity")
    vonP: bool = Field(description="degree of decomposition, vonPost scale, int")
    vonP_top: list[int]
    vonP_bottom: int
    bd_top: float | None
    bd_bottom: float
    peatN: float | None
    peatP: float | None
    peatK: float | None
    enable_peattop: bool
    enable_peatmiddle: bool
    enable_peatbottom: bool
    rho_mor: float = Field(description="bulk density of mor layer, kg m-3")
    h_mor: NonNegativeFloat | Callable[..., float] = Field(
        description="depth of mor layer, m"
    )
    cutting_yr: int = Field(description=" year for cutting")
    cutting_to_ba: float = Field(description="basal area after cutting, m2/ha")
    depoN: float
    depoP: float
    depoK: float
    fertilization: FertilizationParameters

    @computed_field
    @property
    def n(self) -> int:
        # Number of computation nodes in the strip, 2-m width of node
        return int(self.L / 2)

    @computed_field
    @property
    def age(self) -> dict[str, np.ndarray]:
        # Age of stand for all nodes along the strip
        return {
            "dominant": self.initial_dominant_stand_age_years * np.ones(self.n),
            "subdominant": self.initial_subdominant_stand_age_years * np.ones(self.n),
            "under": self.initial_understorey_age_years * np.ones(self.n),
        }

    @computed_field
    @property
    def sfc(self) -> np.ndarray:
        # site fertility class for all nodes along the strip
        return np.ones(self.n, dtype=int) * self.site_fertility_class

    @computed_field
    @property
    def canopylayers(self) -> dict[str, np.ndarray]:
        return {
            "dominant": np.ones(self.n, dtype=int),
            "subdominant": np.zeros(self.n, dtype=int),
            "under": np.zeros(self.n, dtype=int),
        }

    @field_validator("h_mor", mode="before")
    @classmethod
    def compute_if_callable(cls, hmor, info):
        if callable(hmor):
            drain_age = info.data.get("drain_age")
            rho_mor = info.data.get("rho_mor")
            if drain_age is None:
                raise ValueError("`drain_age` must be provided to compute hmor")
            if rho_mor is None:
                raise ValueError("`rho_mor` must be provided to compute hmor")
            try:
                return hmor(drain_age, rho_mor)
            except Exception as e:
                raise ValueError(f"Failed to compute h_mor: {e}")
        return hmor


class Params(StrictFrozenModel):
    paths: MetaData
    simulation_parameters: SimulationParameters
    canopy_parameters: CanopyParameters
    organic_layer_parameters: OrganicLayerParameters
    photo_parameters: PhotoParameters
    output_parameters: OutputParameters


def mass_mor_from_drainage_Pitkanen(drain_age: float) -> float:
    # Pitkänen et al. 2012 Forest Ecology and Management 284 (2012) 100–106
    return 1.616 * np.log(drain_age) - 1.409


def h_mor_from_drainage_and_mass_mor_Pitkanen(
    drain_age: float, rho_mor: float
) -> float:
    return mass_mor_from_drainage_Pitkanen(drain_age) / rho_mor
