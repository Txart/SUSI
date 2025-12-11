import pytest
from pydantic import BaseModel

from susi.io import parameter_creation as pc


class SubSubGroup(BaseModel):
    p2: str


class SubGroup(BaseModel):
    parameterB: float
    parameterC: float
    group2: SubSubGroup


class Config(BaseModel):
    groupA: SubGroup
    learning_rate: float


def test_find_path():
    config = Config(
        groupA=SubGroup(group2=SubSubGroup(p2="lala"), parameterC=2, parameterB=2),
        learning_rate=0.1,
    )
    path = pc.find_path(
        pydantic_model_instance=config, attribute=config.groupA.parameterB
    )
    assert path == ["groupA", "parameterB"]

    path = pc.find_path(pydantic_model_instance=config, attribute=config.groupA)
    assert path == ["groupA"]

    path = pc.find_path(pydantic_model_instance=config, attribute=config)
    assert path == []

    with pytest.raises(Exception):
        path = pc.find_path(pydantic_model_instance=config, attribute=config.groupB)

    # Detects by type, not by value.
    # Works even if two values are identical
    assert config.groupA.parameterB == config.groupA.parameterC
    assert config.groupA.parameterB is not config.groupA.parameterC


def test_set_dict_value_by_key_list():
    d: dict = {"a": 1, "b": {"b1": 2, "b2": 3}}

    modified_d = pc.set_dict_value_by_key_list(d=d, keys=["b", "b1"], value=4)
    d["b"]["b1"] = 4
    assert modified_d == d

    # appends too
    modified_d = pc.set_dict_value_by_key_list(d=d, keys=["b", "c"], value=4)
    d["b"]["c"] = 4
    assert modified_d == d


def test_set_multiple_values_by_key_list():
    d: dict = {"a": 1, "b": {"b1": 2, "b2": 3}}

    keys = [["a"], ["b", "b1"]]
    values = [10, 20]

    modified_d = pc.set_multiple_values_by_key_list(d=d, keys=keys, values=values)
    d["a"] = 10
    d["b"]["b1"] = 20
    assert d == modified_d

    # allows creation of fields
    d = {}
    modified_d = pc.set_multiple_values_by_key_list(d=d, keys=keys, values=values)
    d["a"] = 10
    d["b"] = {"b1": 20}
    assert d == modified_d

    with pytest.raises(Exception):
        less_values = values[:-1]
        pc.set_multiple_values_by_key_list(d=d, keys=keys, values=less_values)

    with pytest.raises(Exception):
        duplicate_keys = [["a"], ["a"]]
        pc.set_multiple_values_by_key_list(d=d, keys=duplicate_keys, values=values)
