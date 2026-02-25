from enclosure_workbench.domain.enclosure_builder import EnclosureBuilder
from enclosure_workbench.domain.parameters import default_parameters


def test_geometry_builder_is_deterministic() -> None:
    builder = EnclosureBuilder()
    params = default_parameters()

    first = builder.build(params)
    second = builder.build(params)

    assert first == second
    assert first.body_outer == (80.0, 50.0, 25.0)
