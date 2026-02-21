# Capability Map

## Purpose

Map current and future enclosure capabilities to stable extension boundaries.

## Capability Matrix

| Capability | Status | Integration Boundary | Notes |
|-----------|--------|----------------------|-------|
| Base enclosure (body + lid) | Implemented (feature 001) | `domain/enclosure_builder.py`, `commands/create_enclosure.py` | Parametric, mm-based defaults and validation |
| Board import | Planned | `integration/` adapter layer | Source expected from KiCad-derived model workflows |
| Screw-hole automation | Planned | `domain/` placement submodule | Depends on board mounting point inputs |
| Connector/component cutout automation | Planned | `domain/` cutout submodule | Depends on protrusion/clearance inputs |

## Rules

- New capabilities MUST map to an existing boundary or add one explicitly.
- Existing `create_enclosure_set` user flow MUST remain backward compatible.
