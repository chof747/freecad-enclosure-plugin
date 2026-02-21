# Tasks: Basic Workbench Scaffold

**Input**: Design documents from `/specs/001-bootstrap-enclosure-workbench/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Testing is explicitly requested in the feature scope; include unit, integration, and contract tasks.

**Organization**: Tasks are grouped by user story so each story remains independently implementable and testable.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize repository structure, tooling, and baseline developer workflow.

- [ ] T001 Create plugin root entry files `Init.py`, `InitGui.py`, and `package.xml`
- [ ] T002 Create package scaffolding under `src/enclosure_workbench/__init__.py` and `src/enclosure_workbench/workbench.py`
- [ ] T003 [P] Create command and domain package scaffolding in `src/enclosure_workbench/commands/` and `src/enclosure_workbench/domain/`
- [ ] T004 [P] Create integration and resources package scaffolding in `src/enclosure_workbench/integration/` and `src/enclosure_workbench/resources/`
- [ ] T005 Create `pyproject.toml` with `uv` workflow and dev dependencies (`pytest`, `flake8`, `debugpy`)
- [ ] T006 [P] Add VS Code workspace configs in `.vscode/launch.json` and `.vscode/extensions.json`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build core abstractions shared by all user stories.

**⚠️ CRITICAL**: No user-story implementation starts before this phase is complete.

- [ ] T007 Create parameter schema and validation module in `src/enclosure_workbench/domain/parameters.py`
- [ ] T008 Create enclosure geometry builder interfaces in `src/enclosure_workbench/domain/enclosure_builder.py`
- [ ] T009 [P] Create FreeCAD document adapter in `src/enclosure_workbench/integration/freecad_document.py`
- [ ] T010 [P] Create object identity/registry adapter in `src/enclosure_workbench/integration/object_registry.py`
- [ ] T011 Implement shared error/result models in `src/enclosure_workbench/domain/results.py`
- [ ] T012 Configure test package structure and `conftest.py` in `tests/conftest.py`
- [ ] T013 [P] Add lint and test command shortcuts in `pyproject.toml` and `README.md`

**Checkpoint**: Foundation ready; user stories can proceed.

---

## Phase 3: User Story 1 - Create a Parametric Project Box (Priority: P1) 🎯 MVP

**Goal**: Provide toolbar and macro entrypoints to create and update enclosure sets (body + lid) with validated parameters.

**Independent Test**: In a clean FreeCAD document, run the toolbar action with defaults, verify body/lid creation, edit parameters in Data section, recompute, and verify deterministic regeneration.

### Tests for User Story 1

- [ ] T014 [P] [US1] Add contract test for `create_enclosure_set` in `tests/contract/test_create_enclosure_set_contract.py`
- [ ] T015 [P] [US1] Add contract test for `update_enclosure_set` in `tests/contract/test_update_enclosure_set_contract.py`
- [ ] T016 [P] [US1] Add unit tests for parameter defaults and validation in `tests/unit/test_parameters.py`
- [ ] T017 [P] [US1] Add unit tests for geometry builder determinism in `tests/unit/test_enclosure_builder.py`
- [ ] T018 [US1] Add integration test for toolbar command flow in `tests/integration/test_create_enclosure_set_command.py`
- [ ] T019 [US1] Add integration test for no writable document behavior in `tests/integration/test_create_enclosure_set_command.py`

### Implementation for User Story 1

- [ ] T020 [US1] Implement `create_enclosure_set` command in `src/enclosure_workbench/commands/create_enclosure.py`
- [ ] T021 [US1] Implement `update_enclosure_set` command in `src/enclosure_workbench/commands/update_enclosure.py`
- [ ] T022 [US1] Implement default parameter provider and validation wiring in `src/enclosure_workbench/domain/parameters.py`
- [ ] T023 [US1] Implement hollow body and lid generation logic in `src/enclosure_workbench/domain/enclosure_builder.py`
- [ ] T024 [US1] Wire command registration and toolbar action in `src/enclosure_workbench/workbench.py`
- [ ] T025 [US1] Implement Data-section property update hook integration in `src/enclosure_workbench/integration/freecad_document.py`
- [ ] T026 [US1] Implement unique enclosure naming/id handling in `src/enclosure_workbench/integration/object_registry.py`

**Checkpoint**: User Story 1 is fully functional and independently testable.

---

## Phase 4: User Story 2 - Start and Install the Workbench Reliably (Priority: P2)

**Goal**: Deliver repeatable packaging, installation, update, deployment, run, and debug workflows for users and maintainers.

**Independent Test**: On a clean profile, install from documented steps, update with documented procedure, open FreeCAD, load workbench, run toolbar action, and attach debugger through VS Code.

### Tests for User Story 2

- [ ] T027 [P] [US2] Add smoke test cases for install/run flow in `tests/integration/test_install_smoke.py`
- [ ] T028 [US2] Add install and update verification tests in `tests/integration/test_install_update_flow.py`

### Implementation for User Story 2

- [ ] T029 [US2] Implement local deployment/install script in `scripts/install-local.sh`
- [ ] T030 [US2] Implement local update script in `scripts/update-local.sh`
- [ ] T031 [US2] Implement FreeCAD smoke-run script in `scripts/smoke-freecad.sh`
- [ ] T032 [US2] Document installation and update procedure in `docs/installation.md`
- [ ] T033 [US2] Document deployment artifact and release procedure in `docs/deployment.md`
- [ ] T034 [US2] Document run and debug procedure using debugpy in `docs/debugging.md`
- [ ] T035 [US2] Update quickstart validation steps in `specs/001-bootstrap-enclosure-workbench/quickstart.md`

**Checkpoint**: User Story 2 is independently installable and verifiable.

---

## Phase 5: User Story 3 - Establish Foundation for Future Enclosure Automation (Priority: P3)

**Goal**: Define architecture boundaries and extension mapping for board-driven future capabilities.

**Independent Test**: Review architecture docs and verify each future capability from `docs/idea.md` maps to a clear extension boundary without changing current user flow.

### Tests for User Story 3

- [ ] T036 [US3] Add architecture consistency checklist in `docs/architecture/review-checklist.md`

### Implementation for User Story 3

- [ ] T037 [US3] Define capability map and statuses in `docs/architecture/capability-map.md`
- [ ] T038 [US3] Define extension boundary contracts in `docs/architecture/extension-boundaries.md`
- [ ] T039 [US3] Define compatibility guarantees for base enclosure flow in `docs/architecture/compatibility.md`
- [ ] T040 [US3] Link architecture artifacts from `docs/idea.md` and `specs/001-bootstrap-enclosure-workbench/spec.md`

**Checkpoint**: User Story 3 architecture baseline is complete and reviewable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final quality gates and cross-story hardening.

- [ ] T041 [P] Execute full lint and test suite with `uv` commands via `pyproject.toml`
- [ ] T042 Validate quickstart end-to-end and capture notes in `specs/001-bootstrap-enclosure-workbench/quickstart.md`
- [ ] T043 [P] Add release and deployment limitations in `docs/release-notes/001-bootstrap-enclosure-workbench.md`
- [ ] T044 [P] Add performance benchmark integration test with thresholds (create <2s, regenerate <1s) in `tests/integration/test_performance_enclosure_flow.py`
- [ ] T045 Record measured create/regenerate timings against thresholds (create <2s, regenerate <1s) in `docs/performance/001-bootstrap-enclosure-workbench.md`
- [ ] T046 [P] Document exact lint and test execution commands/results in `README.md`
- [ ] T047 [P] Update reuse-first dependency decisions and custom-code justifications in `specs/001-bootstrap-enclosure-workbench/research.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) has no dependencies.
- Foundational (Phase 2) depends on Setup completion and blocks all user stories.
- User Stories (Phases 3-5) depend on Foundational completion.
- Polish (Phase 6) depends on completion of selected user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after Phase 2; no dependency on US2/US3.
- **US2 (P2)**: Starts after Phase 2; reuses US1 command entrypoints but remains independently testable.
- **US3 (P3)**: Starts after Phase 2; depends on defined domain/integration boundaries, not US2 deliverables.

### Within Each User Story

- Write story tests before or alongside implementation and verify they fail before final implementation.
- Implement domain/integration internals before command wiring that consumes them.
- Complete story checkpoint before moving to polish.

---

## Parallel Opportunities

- **Setup**: T003, T004, and T006 can run in parallel after T002.
- **Foundational**: T009 and T010 can run in parallel; T013 can run in parallel after T005.
- **US1**: T014-T017 can run in parallel; T020 and T021 can run in parallel after T011.
- **US2**: T029, T030, and T031 can run in parallel; T032, T033, and T034 can run in parallel.
- **US3**: T037, T038, and T039 can run in parallel.
- **Polish**: T041, T043, T044, T046, and T047 can run in parallel.

---

## Parallel Example: User Story 1

```bash
# Contract and unit tests in parallel
Task: "T014 tests/contract/test_create_enclosure_set_contract.py"
Task: "T015 tests/contract/test_update_enclosure_set_contract.py"
Task: "T016 tests/unit/test_parameters.py"
Task: "T017 tests/unit/test_enclosure_builder.py"

# Command implementations in parallel
Task: "T020 src/enclosure_workbench/commands/create_enclosure.py"
Task: "T021 src/enclosure_workbench/commands/update_enclosure.py"
```

## Parallel Example: User Story 2

```bash
Task: "T029 scripts/install-local.sh"
Task: "T030 scripts/update-local.sh"
Task: "T031 scripts/smoke-freecad.sh"
```

## Parallel Example: User Story 3

```bash
Task: "T037 docs/architecture/capability-map.md"
Task: "T038 docs/architecture/extension-boundaries.md"
Task: "T039 docs/architecture/compatibility.md"
```

---

## Implementation Strategy

### MVP First (US1 Only)

1. Complete Phase 1 and Phase 2.
2. Complete Phase 3 (US1).
3. Validate US1 independent test in FreeCAD.
4. Demo MVP before moving to US2/US3.

### Incremental Delivery

1. Setup + Foundational baseline.
2. Deliver US1 (core enclosure workflow).
3. Deliver US2 (install/update/deploy/debug reliability).
4. Deliver US3 (future-proof architecture mapping).
5. Finish with polish and release notes.

### Parallel Team Strategy

1. Team completes Setup and Foundational together.
2. Then split by story:
   - Dev A: US1 command and geometry flow
   - Dev B: US2 deployment/debug workflow
   - Dev C: US3 architecture artifacts

---

## Notes

- `[P]` tasks indicate file-level parallel safety.
- `[US1]`, `[US2]`, `[US3]` tags preserve traceability to spec priorities.
- All tasks include concrete file paths for direct execution.
