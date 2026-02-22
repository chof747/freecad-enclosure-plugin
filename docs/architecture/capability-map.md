# Capability Map

## Purpose

Map current and future enclosure capabilities to stable extension boundaries.

## Capability Matrix

| Capability ID | Status | Integration Boundary | Notes |
|-----------|--------|----------------------|-------|
| `base_enclosure` | `implemented` | `src/enclosure_workbench/domain/enclosure_builder.py`, `src/enclosure_workbench/commands/create_enclosure.py` | Parametric, mm-based defaults and validation |
| `board_import` | `planned` | `src/enclosure_workbench/integration/` adapter layer | Source expected from KiCad-derived model workflows |
| `screw_hole_automation` | `planned` | `src/enclosure_workbench/domain/` placement module | Depends on board mounting point inputs |
| `connector_cutout_automation` | `planned` | `src/enclosure_workbench/domain/` cutout module | Depends on protrusion/clearance inputs |

## Rules

- New capabilities MUST map to an existing boundary or add one explicitly.
- Existing `create_enclosure_set` user flow MUST remain backward compatible.
