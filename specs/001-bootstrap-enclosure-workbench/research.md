# Research: Basic Workbench Scaffold

## Decision 1: Plugin form factor

- Decision: Implement as a FreeCAD workbench with a toolbar command as the first
  user entry point.
- Rationale: The feature requires immediate in-app interaction and aligns with the
  constitution mandate for early FreeCAD-native integration.
- Alternatives considered:
  - Macro-only workflow: faster to prototype, but weaker packaging and discoverability.
  - Headless script only: useful for automation, but does not satisfy toolbar action goal.

## Decision 2: Packaging and environment workflow

- Decision: Use `uv` for dependency syncing and command execution.
- Rationale: Constitution requires reproducible Python tooling with `uv` and
  predictable local setup for contributors.
- Alternatives considered:
  - `pip` + virtualenv: common, but rejected for consistency with constitution.
  - Conda-only environment: adds extra ecosystem dependency not required for MVP.

## Decision 3: Testing strategy

- Decision: Use a layered test strategy: unit tests for parameter rules and geometry
  builders, integration smoke tests for FreeCAD toolbar action, contract tests for
  the documented enclosure action interface.
- Rationale: Balances fast feedback with mandatory in-app integration validation.
- Alternatives considered:
  - Integration-only tests: too slow and hard to isolate failures.
  - Unit-only tests: insufficient for FreeCAD registration/runtime regressions.

## Decision 4: Geometry strategy for MVP enclosure

- Decision: Build the body and lid from deterministic parametric primitives in mm
  with explicit validation on length, width, height, wall thickness, and gap.
- Rationale: Determinism and explicit parameters are central product value and
  required by constitution.
- Alternatives considered:
  - Free-form sketch workflow: flexible but harder to enforce deterministic behavior.
  - Profile-driven presets only: too restrictive for user-entered dimensions.

## Decision 5: Re-run behavior and identity handling

- Decision: Each toolbar invocation creates a new enclosure set with unique identity;
  existing sets remain editable via model Data properties.
- Rationale: Avoids destructive updates and preserves user-generated variants.
- Alternatives considered:
  - Always update existing set: simpler object count, but risks accidental overwrite.
  - Prompt each run for action: adds friction for default user path.

## Decision 6: Scope boundary for this feature

- Decision: Explicitly defer KiCad/board import, screw-hole automation, and connector
  cutout automation to future features while defining extension points now.
- Rationale: Keeps delivery focused on stable scaffold and first value slice.
- Alternatives considered:
  - Include board import now: high risk to timeline and architecture churn.
  - Include placeholders without boundaries: unclear acceptance and test scope.

## Reuse-first update (implementation)

- Reused Python standard library dataclasses and typing for domain contracts.
- Reused pytest and flake8 for test/lint quality gates via `uv run` commands.
- Chose custom minimal FreeCAD adapter abstraction (`integration/freecad_document.py`)
  to isolate host integration and allow deterministic tests without FreeCAD runtime.
