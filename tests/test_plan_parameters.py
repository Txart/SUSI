import pytest

from susi.io import plan_parameters as pp


def test_plan_models():
    """Comprehensive test suite for plan_models function."""
    from pydantic import BaseModel, Field

    # Test Models
    class GroupA(BaseModel):
        parameterB: str = "a"
        parameterC: int = 10

    class MyModel(BaseModel):
        learning_rate: float = 0.01
        batch_size: int = 32
        groupA: GroupA = Field(default_factory=GroupA)

    # Test Basic functionality
    base = MyModel()
    models = pp.plan_models(
        default_model=base,
        set_values={"learning_rate": [0.1, 0.2, 0.3], "batch_size": [64, 128, 256]},
    )
    assert len(models) == 3
    assert models[0].learning_rate == 0.1 and models[0].batch_size == 64
    assert models[1].learning_rate == 0.2 and models[1].batch_size == 128
    assert models[2].learning_rate == 0.3 and models[2].batch_size == 256

    # Test  Nested attributes
    models = pp.plan_models(
        default_model=base,
        set_values={"learning_rate": [0.1, 0.2], "groupA.parameterB": ["b", "c"]},
    )
    assert models[0].groupA.parameterB == "b"
    assert models[1].groupA.parameterB == "c"
    assert models[0].groupA.parameterC == 10  # unchanged

    # Test  Empty set_values
    with pytest.raises(ValueError):
        models = pp.plan_models(default_model=base, set_values={})

    # Test  None set_values
    with pytest.raises(ValueError):
        models = pp.plan_models(default_model=base, set_values=None)

    # Test  Single attribute change
    models = pp.plan_models(
        default_model=base, set_values={"learning_rate": [0.5, 0.6]}
    )
    assert len(models) == 2
    assert models[0].batch_size == 32  # unchanged default

    # Test  Mismatched lengths (should raise ValueError)
    with pytest.raises(ValueError):
        pp.plan_models(
            default_model=base,
            set_values={
                "learning_rate": [0.1, 0.2],
                "batch_size": [64, 128, 256],  # Different length!
            },
        )

    # Test  Invalid attribute path (should raise KeyError)
    with pytest.raises(KeyError):
        pp.plan_models(default_model=base, set_values={"nonexistent_field": [1, 2]})
        assert False, "Should have raised KeyError"

    # Test Invalid nested path (should raise KeyError)
    with pytest.raises(KeyError):
        pp.plan_models(default_model=base, set_values={"groupA.nonexistent": [1, 2]})

    # Test Type validation (should raise ValidationError)
    with pytest.raises(Exception):
        pp.plan_models(
            default_model=base, set_values={"learning_rate": ["not_a_number", 0.2]}
        )

    # Test Deep copy verification (ensure no shared references)
    models = pp.plan_models(
        default_model=base, set_values={"groupA.parameterB": ["x", "y"]}
    )
    models[0].groupA.parameterC = 999
    assert models[1].groupA.parameterC == 10  # Should not be affected

    # Test Tuples and other sequences
    models = pp.plan_models(
        default_model=base,
        set_values={"learning_rate": (0.1, 0.2)},  # Tuple instead of list
    )
    assert len(models) == 2


def test_set_nested_value():
    # Test  Simple single-level path
    data = {"name": "Alice", "age": 30}
    pp._set_nested_value(data, "name", "Bob")
    assert data["name"] == "Bob"
    assert data["age"] == 30  # unchanged

    # Test  Two-level nested path
    data = {"user": {"name": "Alice", "age": 30}}
    pp._set_nested_value(data, "user.name", "Bob")
    assert data["user"]["name"] == "Bob"
    assert data["user"]["age"] == 30

    # Test  Deep nested path (3+ levels)
    data = {"company": {"department": {"team": {"lead": "Alice"}}}}
    pp._set_nested_value(data, "company.department.team.lead", "Bob")
    assert data["company"]["department"]["team"]["lead"] == "Bob"

    # Test  Setting different value types
    data = {"a": 1, "b": {"c": "string"}}
    pp._set_nested_value(data, "a", [1, 2, 3])
    pp._set_nested_value(data, "b.c", {"nested": "dict"})
    assert data["a"] == [1, 2, 3]
    assert data["b"]["c"] == {"nested": "dict"}

    # Test  Invalid top-level key
    data = {"name": "Alice"}
    with pytest.raises(KeyError):
        pp._set_nested_value(data, "nonexistent", "value")

    # Test  Invalid nested key
    data = {"user": {"name": "Alice"}}
    with pytest.raises(KeyError):
        pp._set_nested_value(data, "user.nonexistent", "value")

    # Test  Invalid intermediate key
    data = {"user": {"name": "Alice"}}
    with pytest.raises(KeyError):
        pp._set_nested_value(data, "user.settings.theme", "dark")

    # Test  Non-dict intermediate value
    data = {"user": {"name": "Alice", "age": 30}}
    with pytest.raises(TypeError):
        pp._set_nested_value(data, "user.age.something", "value")

    # Test  Empty path
    data = {"name": "Alice"}
    with pytest.raises(KeyError):
        pp._set_nested_value(data, "", "value")

    # Test  Non-string path
    data = {"name": "Alice"}
    with pytest.raises(Exception):
        pp._set_nested_value(data, 123, "value")  # type: ignore

    # Test  Path with empty key after split
    data = {"name": "Alice"}
    with pytest.raises(Exception):
        pp._set_nested_value(data, "name.", "value")

    # Test  Overwriting with None
    data = {"user": {"name": "Alice"}}
    pp._set_nested_value(data, "user.name", None)
    assert data["user"]["name"] is None

    # Test  Multiple operations on same dict
    data = {"config": {"a": 1, "b": 2, "nested": {"c": 3}}}
    pp._set_nested_value(data, "config.a", 10)
    pp._set_nested_value(data, "config.b", 20)
    pp._set_nested_value(data, "config.nested.c", 30)
    assert data["config"]["a"] == 10
    assert data["config"]["b"] == 20
    assert data["config"]["nested"]["c"] == 30
