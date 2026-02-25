from enclosure_workbench.domain.parameters import (
    ParameterValidationError,
    default_parameters,
    merge_parameters,
    validate_parameters,
)


def test_default_parameters_match_contract() -> None:
    defaults = default_parameters().to_dict()
    assert defaults == {
        "length": 80.0,
        "width": 50.0,
        "height": 25.0,
        "wall_thickness": 2.0,
        "lid_thickness": 3.0,
        "gap": 0.20,
    }


def test_merge_parameters_applies_overrides() -> None:
    merged = merge_parameters({"gap": 0.1, "length": 120.0})
    assert merged.length == 120.0
    assert merged.gap == 0.1
    assert merged.width == 50.0


def test_validation_rejects_invalid_wall_thickness() -> None:
    params = merge_parameters({"wall_thickness": 30.0})
    try:
        validate_parameters(params)
        assert False, "expected ParameterValidationError"
    except ParameterValidationError as exc:
        assert "wall_thickness" in str(exc)
