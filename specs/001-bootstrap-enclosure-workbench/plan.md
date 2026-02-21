# Implementation Plan: Basic Workbench Scaffold

**Branch**: `001-bootstrap-enclosure-workbench` | **Date**: 2026-02-20 | **Spec**: `/Users/chof/playground/cad-ai/freecad-plugin-test/specs/001-bootstrap-enclosure-workbench/spec.md`
**Input**: Feature specification from `/specs/001-bootstrap-enclosure-workbench/spec.md`

## Summary

Deliver a FreeCAD workbench scaffold with packaging and developer workflows, plus a
first toolbar action that creates a parametric enclosure set (hollow body + lid)
using validated parameters in millimeters. The plan keeps KiCad-driven automation
out of scope while establishing architecture boundaries for future expansion.

## Technical Context

**Language/Version**: Python 3.11 (FreeCAD-compatible runtime)  
**Primary Dependencies**: FreeCAD Python API, Part module, PySide (UI), pytest, flake8  
**Storage**: N/A (document-resident parametric objects; optional local config files)  
**Testing**: pytest (unit/integration), FreeCAD smoke tests, `uv run flake8`  
**Target Platform**: FreeCAD desktop on Linux/macOS/Windows  
**Project Type**: Single Python plugin/workbench project  
**Performance Goals**: Initial enclosure creation under 2s for default dimensions; parameter regen under 1s for default dimensions  
**Constraints**: Use `uv` for environment/dependency execution; deterministic geometry from named parameters; no KiCad import in this feature  
**Scale/Scope**: Single-user local design workflow, one workbench, one toolbar action, one enclosure profile

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] FreeCAD-native integration is planned in the earliest deliverable slice.
- [x] Reuse-first analysis is documented; custom code is justified where needed.
- [x] Parametric contract defines names, units, defaults, and validation constraints.
- [x] Clean code quality gate is defined with `uv run flake8`.
- [x] Tooling and dependency commands use `uv` (`uv sync`, `uv run`).

**Gate Status (Pre-Research)**: PASS

## Project Structure

### Documentation (this feature)

```text
specs/001-bootstrap-enclosure-workbench/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
```text
Init.py
InitGui.py
package.xml
.vscode/
└── launch.json

src/
└── enclosure_workbench/
    ├── __init__.py
    ├── workbench.py
    ├── commands/
    │   ├── create_enclosure.py
    │   └── update_enclosure.py
    ├── domain/
    │   ├── parameters.py
    │   └── enclosure_builder.py
    ├── integration/
    │   ├── freecad_document.py
    │   └── object_registry.py
    └── resources/
        ├── icons/
        └── ui/

tests/
├── unit/
│   ├── test_parameters.py
│   └── test_enclosure_builder.py
├── integration/
│   ├── test_create_enclosure_set_command.py
│   ├── test_install_smoke.py
│   ├── test_install_update_flow.py
│   └── test_performance_enclosure_flow.py
└── contract/
    ├── test_create_enclosure_set_contract.py
    └── test_update_enclosure_set_contract.py

scripts/
├── install-local.sh
├── update-local.sh
└── smoke-freecad.sh
```

**Structure Decision**: Single-project Python workbench layout with strict separation
between command/UI layer, parametric domain layer, and FreeCAD integration adapters.

## Phase 0: Research Output

- Research decisions documented in `/Users/chof/playground/cad-ai/freecad-plugin-test/specs/001-bootstrap-enclosure-workbench/research.md`.
- All technical unknowns from this plan are resolved; no open NEEDS CLARIFICATION remains.

## Phase 1: Design & Contracts Output

- Data model documented in `/Users/chof/playground/cad-ai/freecad-plugin-test/specs/001-bootstrap-enclosure-workbench/data-model.md`.
- Command/scripting contract published in `/Users/chof/playground/cad-ai/freecad-plugin-test/specs/001-bootstrap-enclosure-workbench/contracts/enclosure-command-contract.md`.
- Capability map document located at `/Users/chof/playground/cad-ai/freecad-plugin-test/docs/architecture/capability-map.md`.
- Run/install verification captured in `/Users/chof/playground/cad-ai/freecad-plugin-test/specs/001-bootstrap-enclosure-workbench/quickstart.md`.
- VS Code debug attach configuration located at `/Users/chof/playground/cad-ai/freecad-plugin-test/.vscode/launch.json`.
- Agent context updated via `.specify/scripts/bash/update-agent-context.sh opencode`.

## Constitution Check (Post-Design)

- [x] Earliest slice integrates into FreeCAD via toolbar command.
- [x] Reuse-first choices are documented with alternatives in research.
- [x] Parameters, defaults, units, and validations are explicit in data model.
- [x] Lint and quality gates use `uv run flake8` and smoke test path.
- [x] Installation and execution instructions use `uv` workflow.

**Gate Status (Post-Design)**: PASS

## Complexity Tracking

> No constitution violations identified.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |
