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
    body_inner_offset: tuple[float, float, float]
    lid_offset: tuple[float, float, float]
    lip_outer: tuple[float, float, float]
    lip_inner: tuple[float, float, float]
    lip_offset: tuple[float, float, float]


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
        body_inner_offset = (wall, wall, wall)

        lid_offset = (0.0, 0.0, parameters.height + parameters.gap)
        lid_outer = (
            parameters.length,
            parameters.width,
            parameters.lid_thickness,
        )
        lip_height = max(wall, parameters.lid_thickness * 0.6)
        lip_thickness = max(wall * 0.5, 0.6)
        lip_outer_length = parameters.length - (2 * wall) - (2 * parameters.gap)
        lip_outer_width = parameters.width - (2 * wall) - (2 * parameters.gap)
        lip_outer = (lip_outer_length, lip_outer_width, lip_height)

        lip_inner_length = max(lip_outer_length - (2 * lip_thickness), 0.1)
        lip_inner_width = max(lip_outer_width - (2 * lip_thickness), 0.1)
        lip_inner = (lip_inner_length, lip_inner_width, lip_height)

        lip_offset = (
            wall + parameters.gap,
            wall + parameters.gap,
            parameters.height + parameters.gap - lip_height,
        )

        # kept for compatibility with prior contract shape metadata
        lid_inner = (
            lip_inner_length,
            lip_inner_width,
            lip_height,
        )

        return EnclosureGeometry(
            body_outer=body_outer,
            body_inner=body_inner,
            lid_outer=lid_outer,
            lid_inner=lid_inner,
            body_inner_offset=body_inner_offset,
            lid_offset=lid_offset,
            lip_outer=lip_outer,
            lip_inner=lip_inner,
            lip_offset=lip_offset,
        )
