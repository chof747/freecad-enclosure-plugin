"""Parameter defaults and validation for enclosure geometry."""

from __future__ import annotations

from dataclasses import asdict, dataclass


DEFAULT_PARAMETER_VALUES = {
    "length": 80.0,
    "width": 50.0,
    "height": 25.0,
    "wall_thickness": 2.0,
    "lid_thickness": 3.0,
    "gap": 0.20,
}


@dataclass(frozen=True)
class EnclosureParameters:
    length: float
    width: float
    height: float
    wall_thickness: float
    lid_thickness: float
    gap: float

    def to_dict(self) -> dict[str, float]:
        return asdict(self)


class ParameterValidationError(ValueError):
    """Raised when enclosure parameters violate the contract."""


def default_parameters() -> EnclosureParameters:
    return EnclosureParameters(**DEFAULT_PARAMETER_VALUES)


def merge_parameters(
    partial: dict[str, float] | None, base: EnclosureParameters | None = None
) -> EnclosureParameters:
    merged = default_parameters().to_dict() if base is None else base.to_dict()
    if partial:
        merged.update(partial)
    return EnclosureParameters(**merged)


def validate_parameters(parameters: EnclosureParameters) -> None:
    if parameters.length <= 0:
        raise ParameterValidationError("length must be > 0")
    if parameters.width <= 0:
        raise ParameterValidationError("width must be > 0")
    if parameters.height <= 0:
        raise ParameterValidationError("height must be > 0")
    if parameters.wall_thickness <= 0:
        raise ParameterValidationError("wall_thickness must be > 0")

    half_min_dimension = (
        min(parameters.length, parameters.width, parameters.height) / 2.0
    )
    if parameters.wall_thickness >= half_min_dimension:
        raise ParameterValidationError(
            "wall_thickness must be less than half the minimum dimension"
        )
    if parameters.gap < 0:
        raise ParameterValidationError("gap must be >= 0")
    if parameters.gap > parameters.wall_thickness:
        raise ParameterValidationError("gap must be <= wall_thickness")
