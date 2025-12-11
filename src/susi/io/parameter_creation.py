from pydantic import BaseModel
from typing import Any
import copy


def find_path(pydantic_model_instance: BaseModel, attribute) -> list:
    """
    Return the attribute path (as a list) from root to the target value.
    pydantic_model_instance is an instance of a pydantic model.
    Attribute is an attribute of the class.

    Returns error if attribute not in the Pydantic BaseModel.

    Example:

    find_path(root=config, target=config.groupA.group2.p2)
    >>> ['groupA', 'group2', 'p2']
    """
    stack = [(pydantic_model_instance, [])]

    while stack:
        obj, path = stack.pop()

        # If we found the target by identity
        if obj is attribute:
            return path

        # If this is a pydantic model, inspect its fields
        if isinstance(obj, BaseModel):
            for name, value in obj.__dict__.items():
                stack.append((value, path + [name]))

    raise ValueError(
        f"Attribute {attribute} not found in pydantic model instance {pydantic_model_instance}"
    )


def _set_dict_value_by_key_list_inplace(d: dict, keys: list[str], value: Any) -> None:
    """
    # Source - https://stackoverflow.com/a
    # Posted by Bakuriu
    # Retrieved 2025-12-10, License - CC BY-SA 3.0


    """

    for key in keys[:-1]:
        d = d.setdefault(key, {})
    d[keys[-1]] = value


def set_dict_value_by_key_list(d: dict, keys: list[str], value: Any) -> dict:
    """
    Alternative way to set values into dictionary.
    Takes in a list of keys, in order of hierarchy.
    So that:

    my_dict["a"]["b"] = 5

    and

    set_dict_value_by_key_list(my_dict, keys=["a", "b"], value=5)

    are identical.

    (If keys are not found, creates a new entry)

    Example:
    d = {"a": 1, "b": {"b1": 2, "b2":3}}

    modified_d = pc.set_dict_value_by_key_list(d=d, keys=["b", "b1"], value=4)
    d["b"]["b1"] = 4

    assert d == modified_d
    """
    d_copy = copy.deepcopy(d)
    _set_dict_value_by_key_list_inplace(d_copy, keys, value)
    return d_copy


def set_multiple_values_by_key_list(
    d: dict, keys: list[list[str]], values: list
) -> dict:
    """
    Set multiple values to a dictionary in one call.
    Calls set_dict_value_by_key_list() in a loop, with extra catches.

    Error if:
    - (obvious) number of keys != number of values
    - The provided key lists contains duplicates. This is useful to
    prevent unknowingly trying to set the same keys twice in the same call.

    Example:

    d = {}
    keys = [["a"], ["b", "b1"]]
    values = [10, 20]

    modified_d = pc.set_multiple_values_by_key_list(d=d, keys=keys, values=values)
    d["a"] = 10
    d["b"] = {"b1":20}
    """

    if len(keys) != len(values):
        raise ValueError("number of keys must be equal to number of values in list")

    if len(set(map(tuple, keys))) != len(keys):
        raise ValueError("There were duplicated key lists.")

    for key_list, value in zip(keys, values):
        d = set_dict_value_by_key_list(d=d, keys=key_list, value=value)

    return d
