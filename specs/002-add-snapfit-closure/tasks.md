# Tasks: Snap-Fit Closing Mechanism

**Input**: Design documents from `/specs/002-add-snapfit-closure/`
**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/enclosure-command-contract.md`, `quickstart.md`

**Tests**: Included because the feature spec and quickstart define explicit independent test criteria and validation behaviors.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`)
- Every task includes an exact file path

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare shared test/util scaffolding and keep contracts/docs aligned before core implementation.

- [ ] T001 Add snap-fit shared payload fixtures in `tests/conftest.py`
- [ ] T002 [P] Add validation assertion helpers for warning/error payloads in `tests/unit/test_parameters.py`
- [ ] T003 [P] Align command contract examples with execution-ready test cases in `specs/002-add-snapfit-closure/contracts/enclosure-command-contract.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core model and adapter plumbing required before any user story work.

**⚠️ CRITICAL**: No user story work starts until this phase is complete.

- [ ] T004 Extend parameter domain with closing mechanism and snap-fit config dataclasses in `src/enclosure_workbench/domain/parameters.py`
- [ ] T005 Add clamp result model and warning payload support in `src/enclosure_workbench/domain/results.py`
- [ ] T006 Update persisted enclosure record fields for mechanism/snap-fit metadata in `src/enclosure_workbench/integration/enclosure_record.py`
- [ ] T007 Update adapter protocol for mechanism-aware updates and warning propagation in `src/enclosure_workbench/integration/document_adapter.py`
- [ ] T008 [P] Implement foundational persistence updates for in-memory adapter in `src/enclosure_workbench/integration/in_memory_document.py`
- [ ] T009 [P] Implement foundational persistence updates for FreeCAD adapter in `src/enclosure_workbench/integration/freecad_document.py`
- [ ] T010 Add/adjust feature-object data-section synchronization for new parameters in `src/enclosure_workbench/integration/enclosure_feature.py`

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Enable snap-fit closure (Priority: P1) 🎯 MVP

**Goal**: Selecting `snap_fit` generates matching body/lid closure geometry that is reversible.

**Independent Test**: Create enclosure with `closing_mechanism = snap_fit`; confirm matching closure geometry appears on body/lid and create/update command contracts remain valid.

### Tests for User Story 1

- [ ] T011 [P] [US1] Add create contract test for `closing_mechanism = snap_fit` success payload in `tests/contract/test_create_enclosure_set_contract.py`
- [ ] T012 [P] [US1] Add update contract test for `closing_mechanism = snap_fit` persistence in `tests/contract/test_update_enclosure_set_contract.py`
- [ ] T013 [P] [US1] Add geometry unit tests for snap-fit feature generation in `tests/unit/test_enclosure_builder.py`
- [ ] T014 [P] [US1] Add integration test for snap-fit create flow in `tests/integration/test_create_enclosure_set_command.py`

### Implementation for User Story 1

- [ ] T015 [US1] Run early FreeCAD smoke validation for `Create Enclosure` command path in `tests/integration/test_install_smoke.py`
- [ ] T016 [P] [US1] Implement snap-fit geometry primitives and placement helpers in `src/enclosure_workbench/domain/enclosure_builder.py`
- [ ] T017 [US1] Integrate snap-fit mechanism selection into create command flow in `src/enclosure_workbench/commands/create_enclosure.py`
- [ ] T018 [US1] Integrate snap-fit mechanism selection into update command flow in `src/enclosure_workbench/commands/update_enclosure.py`
- [ ] T019 [US1] Ensure FreeCAD object generation includes snap-fit geometry outputs in `src/enclosure_workbench/integration/freecad_document.py`

**Checkpoint**: US1 is independently functional and testable (MVP).

---

## Phase 4: User Story 2 - Keep closures optional (Priority: P2)

**Goal**: `none` keeps current open-fit behavior and backward compatibility.

**Independent Test**: Generate enclosure with `closing_mechanism = none` (and with missing mechanism field in legacy-style input) and verify no snap-fit geometry is produced.

### Tests for User Story 2

- [ ] T020 [P] [US2] Add create contract test for `closing_mechanism = none` geometry omission in `tests/contract/test_create_enclosure_set_contract.py`
- [ ] T021 [P] [US2] Add backward-compat contract test for missing mechanism defaulting to `none` in `tests/contract/test_update_enclosure_set_contract.py`
- [ ] T022 [P] [US2] Add integration test for none-mode behavior in create/update flow in `tests/integration/test_install_update_flow.py`

### Implementation for User Story 2

- [ ] T023 [US2] Implement explicit none-mode geometry suppression path in builder/command boundary in `src/enclosure_workbench/domain/enclosure_builder.py`
- [ ] T024 [US2] Enforce backward-compatible default-to-none behavior in parameter merge logic in `src/enclosure_workbench/domain/parameters.py`
- [ ] T025 [US2] Preserve none-mode semantics in FreeCAD feature updates in `src/enclosure_workbench/integration/enclosure_feature.py`

**Checkpoint**: US2 works independently and does not regress existing workflows.

---

## Phase 5: User Story 3 - Adjust snap-fit behavior with defaults (Priority: P3)

**Goal**: Snap-fit parameters are defaulted, user-adjustable, clamped with warnings, and blocked when impossible.

**Independent Test**: Initialize Snap-Fit defaults, modify values, verify geometry updates; confirm out-of-range values clamp with warnings and impossible cases return validation error; verify snap-fit values restore after toggle none->snap_fit.

### Tests for User Story 3

- [ ] T026 [P] [US3] Add unit tests for snap-fit default values and bounds in `tests/unit/test_parameters.py`
- [ ] T027 [P] [US3] Add contract tests for clamped warning payload shape in `tests/contract/test_update_enclosure_set_contract.py`
- [ ] T028 [P] [US3] Add contract test for blocking dimensional validation error after clamping in `tests/contract/test_update_enclosure_set_contract.py`
- [ ] T029 [P] [US3] Add integration test for snap-fit parameter restore on mechanism toggle in `tests/integration/test_install_update_flow.py`

### Implementation for User Story 3

- [ ] T030 [US3] Implement snap-fit defaults, clamp logic, and blocking constraints in `src/enclosure_workbench/domain/parameters.py`
- [ ] T031 [US3] Emit warning-aware command payload status and warning entries in `src/enclosure_workbench/commands/update_enclosure.py`
- [ ] T032 [US3] Emit warning-aware command payload status and warning entries in `src/enclosure_workbench/commands/create_enclosure.py`
- [ ] T033 [US3] Persist and restore snap-fit parameter state across mechanism toggles in `src/enclosure_workbench/integration/in_memory_document.py`
- [ ] T034 [US3] Persist and restore snap-fit parameter state across mechanism toggles in `src/enclosure_workbench/integration/freecad_document.py`

**Checkpoint**: US3 is independently functional and testable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Hardening, documentation, and full validation across stories.

- [ ] T035 [P] Update developer-facing behavior notes for mechanism/clamp/fail semantics in `docs/`
- [ ] T036 Add/refresh docstrings for all changed classes, methods, and functions in `src/enclosure_workbench/`
- [ ] T037 Add user-facing parameter descriptions for closing mechanism and snap-fit settings in `docs/snapfit-parameters.md`
- [ ] T038 Run and fix lint issues using `uv run flake8` for touched modules in `src/enclosure_workbench/`
- [ ] T039 Run full automated validation suite from quickstart plus representative size-matrix checks for SC-002 in `tests/unit/`, `tests/contract/`, and `tests/integration/`
- [ ] T040 Run timed user acceptance validation for SC-003 and capture results in `specs/002-add-snapfit-closure/checklists/usability-results.md`
- [ ] T041 Run bench open/close cycle validation for SC-004 and capture results in `specs/002-add-snapfit-closure/checklists/bench-results.md`
- [ ] T042 Validate final FreeCAD smoke regression for create/update + none/snap-fit switching via `src/enclosure_workbench/workbench.py` command path

---

## Dependencies & Execution Order

### Phase Dependencies

- Setup (Phase 1) -> Foundational (Phase 2) -> User Stories (Phases 3-5) -> Polish (Phase 6)

### User Story Dependencies

- **US1 (P1)**: starts after Foundational; no dependency on US2/US3
- **US2 (P2)**: starts after Foundational; independent from US1 implementation details
- **US3 (P3)**: starts after Foundational; depends on baseline snap-fit mechanism support from US1

### Suggested Story Completion Order

1. US1 (MVP)
2. US2 (backward compatibility and optional mode)
3. US3 (parameter tuning/clamping/restore behaviors)

---

## Parallel Opportunities

- **Setup**: T002 and T003
- **Foundational**: T008 and T009
- **US1**: T011-T014 can run in parallel; T016 can proceed while tests are prepared
- **US2**: T020-T022 can run in parallel
- **US3**: T026-T029 can run in parallel; T033 and T034 can run in parallel

---

## Parallel Example: User Story 1

```bash
Task: "T011 [US1] Add create contract test in tests/contract/test_create_enclosure_set_contract.py"
Task: "T012 [US1] Add update contract test in tests/contract/test_update_enclosure_set_contract.py"
Task: "T013 [US1] Add geometry unit tests in tests/unit/test_enclosure_builder.py"
Task: "T014 [US1] Add integration flow test in tests/integration/test_create_enclosure_set_command.py"
```

## Parallel Example: User Story 3

```bash
Task: "T026 [US3] Add defaults/bounds unit tests in tests/unit/test_parameters.py"
Task: "T027 [US3] Add clamping warning contract tests in tests/contract/test_update_enclosure_set_contract.py"
Task: "T029 [US3] Add toggle restore integration test in tests/integration/test_install_update_flow.py"
```

---

## Implementation Strategy

### MVP First (US1 only)

1. Complete Phase 1 and Phase 2
2. Complete US1 (Phase 3)
3. Validate US1 independent test criteria and contract outputs

### Incremental Delivery

1. Deliver US1 (Snap-Fit core)
2. Deliver US2 (none mode + backward compatibility)
3. Deliver US3 (tuning/clamping/restore)
4. Finish with Phase 6 polish and full validation
