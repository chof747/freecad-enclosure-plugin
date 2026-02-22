<!--
Sync Impact Report
- Version change: 1.0.0 -> 1.1.0
- Modified principles:
  - IV. Clean Code with Mandatory Lint Gates -> IV. Clean Code, Mandatory Docstrings,
    and Lint Gates
- Added sections:
  - None
- Removed sections:
  - None
- Templates requiring updates:
  - ✅ updated: .specify/templates/plan-template.md
  - ✅ updated: .specify/templates/spec-template.md
  - ✅ updated: .specify/templates/tasks-template.md
  - ✅ reviewed (no change needed): .opencode/command/speckit.constitution.md
  - ✅ updated: README.md
  - ✅ updated: AGENTS.md
- Follow-up TODOs:
  - None
-->

# FreeCAD Enclosure Plugin Constitution

## Core Principles

### I. FreeCAD-Native Integration First
Every feature MUST integrate with the FreeCAD runtime early, not only at the end.
Each feature plan MUST include an in-app execution path (for example, command,
toolbar action, or workbench action) that is validated by a smoke run in FreeCAD
before feature completion. Rationale: early integration reduces API mismatch and
GUI/runtime breakage discovered late in delivery.

### II. Library-First and Reuse-First Engineering
Implementation MUST prefer existing capabilities in the Python standard library,
FreeCAD APIs, and mature third-party packages before adding custom utility code.
When custom code is necessary, the feature plan MUST document why reusable options
are insufficient and what boundary the custom code owns. Rationale: reuse lowers
maintenance cost and improves reliability.

### III. Parametric Integrity for Enclosure Models
Enclosure geometry MUST be generated from explicit, named parameters with defined
units, default values, and validation constraints. Geometry builders MUST be
deterministic for the same parameter set and MUST avoid hidden shape constants.
Rationale: deterministic parametric behavior is the core value of enclosure design.

### IV. Clean Code, Mandatory Docstrings, and Lint Gates
All Python changes MUST pass `flake8` with project configuration before merge.
Code MUST keep clear module boundaries (UI command wiring, parametric domain logic,
and FreeCAD integration adapters separated) and avoid dead code. All classes,
methods, and functions added or modified in feature work MUST include meaningful
docstrings that explain purpose and behavior. Rationale: clean, linted, and
well-documented code keeps plugin evolution safe as feature complexity grows.

### V. Reproducible Python Tooling with uv
Dependency management and Python command execution MUST use `uv` (`uv sync`,
`uv run ...`) in docs, scripts, and CI tasks. Direct `pip` workflows are not
allowed unless a FreeCAD platform constraint makes `uv` impossible and the
exception is documented in the plan. Rationale: reproducible environments reduce
onboarding and build drift.

## Technical Standards

- The plugin runtime target is Python in the active FreeCAD release line.
- Workbench or command registration MUST be present for user-facing features.
- Parametric APIs MUST define stable parameter names to preserve model reuse.
- Static analysis baseline MUST include `flake8` and pass before review completion.
- Python classes, methods, and functions MUST include descriptive docstrings.
- Project scripts and instructions MUST prefer `uv` commands for consistency.

## Development Workflow & Quality Gates

1. Capture feature intent and parameter contract in the feature specification.
2. Plan implementation with a Constitution Check that verifies all five principles.
3. Build the smallest usable FreeCAD integration slice first.
4. Add or extend domain logic using reuse-first library selection.
5. Run quality gates: lint via `uv run flake8`, verify docstrings on changed
   classes/methods/functions, and execute a FreeCAD integration smoke run.
6. Complete review only when constitution compliance is explicitly confirmed.

## Governance

This constitution overrides conflicting local practices for this repository.
Amendments require (a) a written change in this file, (b) an updated Sync Impact
Report, and (c) updates to affected templates and workflow guidance in the same
change set.

Versioning policy for this constitution follows semantic versioning:
- MAJOR: removes or redefines a principle or governance rule incompatibly.
- MINOR: adds a new principle/section or materially expands required behavior.
- PATCH: clarifies wording without changing required behavior.

Compliance review is required in every implementation plan and pull request.
Reviewers MUST block merge when constitution gates are unmet or evidence is absent.

**Version**: 1.1.0 | **Ratified**: 2026-02-19 | **Last Amended**: 2026-02-22
