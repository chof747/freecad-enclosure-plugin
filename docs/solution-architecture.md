# Solution Architecture Guide

This document explains the main components of the Enclosure workbench, their responsibilities, and how they interact at runtime.

## High-Level Architecture

The plugin is organized into three layers:

- `commands/`: user-facing operations (create, update, toggle visibility)
- `domain/`: parameter validation and deterministic geometry calculations
- `integration/`: FreeCAD-specific object/document integration (FeaturePython, adapters, view provider)

Entry points:

- `InitGui.py`: legacy compatibility loader
- `freecad/enclosure_workbench/init_gui.py`: main FreeCAD GUI registration

## Component Map

### GUI and Workbench Registration

- `freecad/enclosure_workbench/init_gui.py`
  - Registers workbench and toolbar commands.
  - Provides:
    - `CreateEnclosure`
    - `ToggleEnclosureBody`
    - `ToggleEnclosureLid`
- `InitGui.py`
  - Lightweight compatibility entrypoint that forwards to modern registration.

### Commands Layer

- `src/enclosure_workbench/commands/create_enclosure.py`
  - Validates/merges inputs, allocates identity, builds geometry metadata, creates document object.
- `src/enclosure_workbench/commands/update_enclosure.py`
  - Updates an existing enclosure by id with new parameters.
- `src/enclosure_workbench/commands/toggle_enclosure_visibility.py`
  - Toggles body/lid visibility flags for a selected enclosure object.

### Domain Layer

- `src/enclosure_workbench/domain/parameters.py`
  - Defines `EnclosureParameters` and defaults.
  - Owns validation rules for dimensions and gap constraints.
- `src/enclosure_workbench/domain/enclosure_builder.py`
  - Single source of truth for derived dimensions/offsets used to construct geometry.
  - Returns `EnclosureGeometry` with body/lid/lip dimensions and placements.
- `src/enclosure_workbench/domain/results.py`
  - Command result envelope (`success`/`failure`) and error shapes.

### Integration Layer

- `src/enclosure_workbench/integration/freecad_document.py`
  - Real adapter around FreeCAD document access and object lifecycle.
  - Creates and updates `Part::FeaturePython` enclosure objects.
  - Bridges command-level ids/records to actual document objects.
- `src/enclosure_workbench/integration/in_memory_document.py`
  - Test/headless adapter that mimics persistence without requiring a FreeCAD document.
  - Used by automated tests to keep command contracts deterministic.
- `src/enclosure_workbench/integration/enclosure_feature.py`
  - `EnclosureFeatureProxy`: FeaturePython proxy with Data properties and `execute()` recompute logic.
  - `EnclosureViewProvider`: icon/view behavior.
- `src/enclosure_workbench/integration/object_registry.py`
  - Generates stable unique enclosure ids/names and avoids naming collisions.

## Runtime Flows

### 1) Create Enclosure (toolbar)

1. User clicks `Create Enclosure`.
2. GUI command calls `create_enclosure_set(...)`.
3. Command:
   - merges defaults + overrides
   - validates parameters
   - allocates unique identity
   - computes geometry metadata via `EnclosureBuilder`
4. `FreeCADDocumentAdapter` creates a `Part::FeaturePython` object.
5. `EnclosureFeatureProxy` is attached; Data properties are set.
6. Document recompute triggers `execute()` and generates final shape (body + lid).

### 2) Edit Parameters in Data Section

1. User edits `Length`, `Width`, `Height`, `WallThickness`, `LidThickness`, or `Gap`.
2. FreeCAD recompute calls `EnclosureFeatureProxy.execute()`.
3. `execute()`:
   - reads Data properties
   - validates parameters
   - reuses `EnclosureBuilder.build(...)` for derived dimensions
   - rebuilds body/lid shape and assigns `fp.Shape`.

### 3) Toggle Body/Lid Visibility

1. User selects one enclosure object.
2. User clicks toggle command.
3. Command calls `toggle_enclosure_visibility(id, target)`.
4. Adapter flips `ShowBody` and/or `ShowLid`.
5. Recompute updates shape composition accordingly.

## Parameter Semantics

Canonical units are millimeters.

Important geometry rule:

- Lid and body outer X/Y footprint are equal.
- `gap` affects mating clearance between body and lid interface, not outer lid enlargement.

## Extension Points for Developers

- Add new user actions in `freecad/enclosure_workbench/init_gui.py`.
- Add command behavior in `src/enclosure_workbench/commands/`.
- Keep geometric formulas centralized in `src/enclosure_workbench/domain/enclosure_builder.py`.
- Keep FreeCAD object-manipulation code in `src/enclosure_workbench/integration/`.

## Notes and Conventions

- Use command result envelopes for user-visible failures.
- Keep domain logic deterministic and FreeCAD-independent where possible.
- Prefer updating existing FeaturePython properties and recompute rather than rebuilding unrelated objects.
