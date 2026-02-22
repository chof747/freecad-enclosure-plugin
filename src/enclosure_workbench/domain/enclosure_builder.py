"""Deterministic enclosure geometry builder abstraction."""

from __future__ import annotations

from dataclasses import dataclass

from .parameters import EnclosureParameters


@dataclass(frozen=True)
class EnclosureGeometry:
    body_outer: tuple[float, float, float]
    body_inner: tuple[float, float, float]
    lid_outer: tuple[float, float, float]
    lid_inner: tuple[float, float, float]


class EnclosureBuilder:
    """Build deterministic geometry descriptors from validated parameters."""

    def build(self, parameters: EnclosureParameters) -> EnclosureGeometry:
        wall = parameters.wall_thickness
        body_outer = (parameters.length, parameters.width, parameters.height)
        body_inner = (
            parameters.length - (2 * wall),
            parameters.width - (2 * wall),
            parameters.height - wall,
        )

        lid_height = max(wall * 2.0, parameters.height * 0.2)
        lip_wall = max(wall - parameters.gap, 0.01)
        lid_outer = (
            parameters.length + (2 * parameters.gap),
            parameters.width + (2 * parameters.gap),
            lid_height,
        )
        lid_inner = (
            parameters.length - (2 * lip_wall),
            parameters.width - (2 * lip_wall),
            lid_height - lip_wall,
        )

        return EnclosureGeometry(
            body_outer=body_outer,
            body_inner=body_inner,
            lid_outer=lid_outer,
            lid_inner=lid_inner,
        )
