from typing import TypeVar, Any, Sequence
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


def plan_models(
    default_model: T, set_values: dict[str, Sequence[Any]] | None = None
) -> list[T]:
    """
    Create multiple model instances by setting different values for specified attributes.

    Args:
        default_model: A Pydantic model instance to use as the base
        set_values: Dict mapping attribute paths (dot notation) to sequences of values.
                   All sequences must have the same length.

    Returns:
        List of model instances with values set according to set_values

    Raises:
        ValueError: If value sequences have different lengths
        KeyError: If an attribute path doesn't exist in the model
        ValidationError: If a value fails Pydantic validation

    Example:
        >>> from pydantic import BaseModel
        >>>
        >>> class Config(BaseModel):
        ...     learning_rate: float = 0.01
        ...     batch_size: int = 32
        >>>
        >>> base = Config()
        >>> models = plan_models(
        ...     default_model=base,
        ...     set_values={
        ...         "learning_rate": [0.1, 0.2],
        ...         "batch_size": [64, 128]
        ...     }
        ... )
        >>> len(models)
        2
    """
    if set_values is None or not set_values:
        raise ValueError(
            "set_values must not be empty. If you really want to set nothing, just use the default model."
        )

    # Validate all sequences have the same length
    lengths = {len(values) for values in set_values.values()}
    if len(lengths) > 1:
        length_info = {k: len(v) for k, v in set_values.items()}
        raise ValueError(
            f"All value sequences must have the same length. Got: {length_info}"
        )

    num_models = lengths.pop()
    models = []

    for i in range(num_models):
        # Deep copy to avoid shared mutable objects
        model_dict = default_model.model_dump()

        # Apply the i-th value from each attribute path
        for attr_path, values in set_values.items():
            try:
                _set_nested_value(model_dict, attr_path, values[i])
            except KeyError as e:
                raise KeyError(
                    f"Attribute path '{attr_path}' not found in model {type(default_model).__name__}"
                ) from e

        # Validate and create new model instance
        try:
            models.append(type(default_model)(**model_dict))
        except ValidationError:
            raise ValidationError(f"Pydantic validation failed for model number {i}")
    return models


def _set_nested_value(d: dict, path: str, value: Any) -> None:
    """
    Set a value in a nested dictionary using dot notation path.

    Raises:
        KeyError: If any key in the path doesn't exist
    """
    keys = path.split(".")
    current = d

    for key in keys[:-1]:
        if key not in current:
            raise KeyError(f"Key '{key}' not found in path '{path}'")
        current = current[key]

    final_key = keys[-1]
    if final_key not in current:
        raise KeyError(f"Key '{final_key}' not found in path '{path}'")

    current[final_key] = value
