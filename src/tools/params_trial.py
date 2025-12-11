from pydantic import BaseModel

from susi.io import parameter_creation


class SubSubGroup(BaseModel):
    p2: str


class SubGroup(BaseModel):
    parameterB: int
    parameterC: float
    group2: SubSubGroup


class Config(BaseModel):
    groupA: SubGroup
    learning_rate: float


# %% call

config = Config(
    groupA=SubGroup(group2=SubSubGroup(p2="lala"), parameterC=1, parameterB=2),
    learning_rate=0.1,
)

md = config.model_dump()
nested = parameter_creation.find_path(
    pydantic_model_instance=config, attribute=config.groupA.group2.p2
)

parameter_creation.set_dict_value_by_key_list(md, keys=nested, value="lali")

# %% Multiple keys

md = config.model_dump()
multiple_nested = [
    parameter_creation.find_path(
        pydantic_model_instance=config, attribute=config.groupA.group2.p2
    ),
    parameter_creation.find_path(
        pydantic_model_instance=config, attribute=config.groupA.parameterB
    ),
]

# %% TODO test new way of asigning parameters
