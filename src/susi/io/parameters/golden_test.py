import datetime
from susi.config import (
    Params,
    MetaData,
    SimulationParameters,
    TreeSpecies,
    NutrientFertilizationParameters,
    FertilizationParameters,
    CanopyParameters,
    OrganicLayerParameters,
    LocationsForPhotoParams,
    get_photo_parameters_by_location,
    OutputParameters,
    h_mor_from_drainage_and_mass_mor_Pitkanen,
)

PARAMETERS = Params(
    paths=MetaData(),
    canopy_parameters=CanopyParameters(),
    organic_layer_parameters=OrganicLayerParameters(),
    photo_parameters=get_photo_parameters_by_location(
        location=LocationsForPhotoParams("All_data")
    ),
    output_parameters=OutputParameters(),
    simulation_parameters=SimulationParameters(
        start_date=datetime.datetime(2004, 1, 1),
        end_date=datetime.datetime(2005, 12, 31),
        L=40.0,
        initial_dominant_stand_age_years=100.0,
        initial_subdominant_stand_age_years=0.0,
        initial_understorey_age_years=0.0,
        site_fertility_class=4,
        sitename="susirun",
        species=TreeSpecies("Pine"),
        sfc_specification=1,
        hdom=None,
        vol=None,
        smc="Peatland",
        nLyrs=60,
        dzLyr=0.05,
        ditch_depth_west=[-0.5],
        ditch_depth_east=[-0.5],
        ditch_depth_20y_west=[-0.5],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
        ditch_depth_20y_east=[-0.5],  # ojan syvyys 20 vuotta simuloinnin aloituksesta
        scenario_name=["D60"],  # kasvunlisaykset
        drain_age=100,
        initial_h=-0.2,
        slope=0.0,
        peat_type=["A", "A", "A", "A", "A", "A", "A", "A"],
        peat_type_bottom=["A"],
        anisotropy=10.0,
        vonP=True,
        vonP_top=[2, 2, 2, 3, 4, 5, 6, 6],
        vonP_bottom=8,
        bd_top=None,
        bd_bottom=0.16,
        peatN=None,
        peatP=None,
        peatK=None,
        enable_peattop=True,
        enable_peatmiddle=True,
        enable_peatbottom=True,
        rho_mor=80.0,  # bulk density of mor layer, kg m-3
        h_mor=h_mor_from_drainage_and_mass_mor_Pitkanen,
        cutting_yr=2001,  # year for cutting
        cutting_to_ba=12,  # basal area after cutting, m2/ha
        depoN=4.0,
        depoP=0.1,
        depoK=1.0,
        fertilization=FertilizationParameters(
            application_year=2201,
            N=NutrientFertilizationParameters(
                dose=0.0,
                decay_k=0.5,
                eff=1.0,
            ),  # fertilization dose in kg ha-1, decay_k in yr-1
            P=NutrientFertilizationParameters(dose=45.0, decay_k=0.2, eff=1.0),
            K=NutrientFertilizationParameters(dose=100.0, decay_k=0.3, eff=1.0),
            pH_increment=1.0,
        ),
    ),
)
