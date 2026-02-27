# freecad-plugin-test Development Guidelines

Auto-generated from all feature plans. Last updated: 2026-02-20

## Active Technologies
- Python 3.11 (FreeCAD runtime target) + FreeCAD Python API, Part module, existing `enclosure_workbench` domain/integration layers (002-add-snapfit-closure)
- FreeCAD document objects and in-memory command payloads (no external database) (002-add-snapfit-closure)

- Python 3.11 (FreeCAD-compatible runtime) + FreeCAD Python API, Part module, PySide (UI), pytest, flake8 (001-bootstrap-enclosure-workbench)

## Project Structure

```text
src/
tests/
```

## Commands

cd src [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] pytest [ONLY COMMANDS FOR ACTIVE TECHNOLOGIES][ONLY COMMANDS FOR ACTIVE TECHNOLOGIES] ruff check .

## Code Style

Python 3.11 (FreeCAD-compatible runtime): Follow standard conventions

## Recent Changes
- 002-add-snapfit-closure: Added Python 3.11 (FreeCAD runtime target) + FreeCAD Python API, Part module, existing `enclosure_workbench` domain/integration layers

- 001-bootstrap-enclosure-workbench: Added Python 3.11 (FreeCAD-compatible runtime) + FreeCAD Python API, Part module, PySide (UI), pytest, flake8

<!-- MANUAL ADDITIONS START -->
- Code documentation rule: Add docstrings for classes, methods, and functions that are introduced or modified.
- Contract format rule: Use in-process Markdown command contracts under `specs/*/contracts/`; avoid OpenAPI/GraphQL unless a feature explicitly adds an external HTTP API (see `.specify/memory/contract-conventions.md`).
<!-- MANUAL ADDITIONS END -->
