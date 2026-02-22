# Feature Specification: Basic Workbench Scaffold

**Feature Branch**: `001-bootstrap-enclosure-workbench`  
**Created**: 2026-02-19  
**Status**: Draft  
**Input**: User description: "basic-structure: I want to start with a basic plugin or workbench structure whatever fits best which should 1. Create the projects scaffold 2. Setup the packaging, deployment and installation procedure 3. Sets up all the necessary testing, run and debugging configurations 4. Has as a first feature a user action (in a toolbar) that creates a simple project box consiting of a hollow body and a matching lit with basic parameters of length, width, height, wall thickness, lid thickness and gap (to define 3d printing tolerances) In the course of this feature I also want to define the basic architecture of the overall solution for the overall idea sketched in @docs/idea.md"

## Clarifications

### Session 2026-02-20

- Q: What should happen when the toolbar action is run again in the same document? -> A: Always create a new body+lid set; existing sets remain editable via the model view Data section.
- Q: What unit system should be canonical for enclosure parameters? -> A: Millimeters (mm) are canonical for all enclosure parameters.
- Q: Should the first release provide parameter defaults or require manual entry each time? -> A: Provide fixed MVP defaults for all five parameters.
- Q: What exact MVP default values should be used for length, width, height, wall thickness, and gap? -> A: L=80 mm, W=50 mm, H=25 mm, wall=2.0 mm, gap=0.20 mm.
- Q: Are KiCad/board-import and enclosure automation capabilities included in this feature release? -> A: No; board import, screw-hole automation, and connector cutout automation are out of scope for this feature.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Parametric Project Box (Priority: P1)

As a FreeCAD user, I can trigger a toolbar action that creates a simple enclosure
set consisting of a hollow box body and a matching lid using editable base
parameters so I can quickly start a printable project enclosure.

**Why this priority**: This is the first user-visible value and proves the core
parametric enclosure outcome in a single workflow.

**Independent Test**: In a clean document, run the toolbar action, verify one
parametric enclosure object is created in the model tree, edit length/width/height/
wall thickness/lid thickness/gap in its Data section, and verify both body and lid geometry
regenerate from that single object.

**Acceptance Scenarios**:

1. **Given** an open FreeCAD document, **When** the user runs the enclosure toolbar
   action with valid parameters, **Then** the system creates one parametric enclosure
   object that generates one hollow body and one matching lid.
2. **Given** an already generated enclosure, **When** the user updates one parameter
   value, **Then** both body and lid update consistently without manual remodeling.
3. **Given** one or more existing enclosure sets, **When** the user runs the toolbar
   action again, **Then** a new enclosure set is created and existing sets remain
   editable in the model view Data section.

---

### User Story 2 - Start and Install the Workbench Reliably (Priority: P2)

As a maintainer or user, I can install and launch the workbench from a documented
procedure so that the feature is usable in a repeatable way across fresh setups.

**Why this priority**: Without reliable packaging and installation, the feature
cannot be adopted or validated by others.

**Independent Test**: On a fresh environment, follow documented install and launch
steps, open FreeCAD, and confirm the workbench and toolbar action are available.

**Acceptance Scenarios**:

1. **Given** a clean machine profile, **When** the user follows the documented
   installation procedure, **Then** the workbench loads successfully and exposes the
   enclosure creation action.
2. **Given** an updated plugin package, **When** the user applies the documented
   update procedure, **Then** the prior installation upgrades without manual
   restructuring of project files.

---

### User Story 3 - Establish Foundation for Future Enclosure Automation (Priority: P3)

As a product owner, I can review a defined baseline architecture and extension
boundaries so future capabilities from `docs/idea.md` (board-driven enclosure,
screw holes, connector cutouts) can be added without reworking the foundation.

**Why this priority**: This protects early work from expensive refactors and keeps
the first release aligned with the longer-term enclosure automation direction.

**Independent Test**: Review the architecture definition and confirm it identifies
major modules, extension points, and how future board-derived features fit into the
existing model-generation workflow.

**Acceptance Scenarios**:

1. **Given** the initial scaffold is complete, **When** stakeholders review the
   baseline architecture artifact, **Then** they can trace where future board import,
   screw-hole placement, and connector cutout capabilities will integrate.
2. **Given** a proposed follow-up feature from `docs/idea.md`, **When** maintainers
   map it to the defined architecture, **Then** they can add it without changing the
   public user flow for creating a base enclosure.

---

### Edge Cases

- User enters zero, negative, or non-numeric values for enclosure parameters.
- Wall thickness is too large for the provided outer dimensions.
- Gap value causes lid-body overlap or excessive looseness beyond acceptable range.
- Toolbar action is triggered without an active writable document.
- Re-running the action in the same document risks duplicate names or object clashes.
- Parameter update would produce non-manifold or otherwise invalid geometry.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a project scaffold that separates user actions,
  parametric enclosure generation logic, and extension-oriented domain boundaries.
- **FR-002**: System MUST provide a user-visible toolbar action that starts enclosure
  creation in an open FreeCAD session.
- **FR-003**: System MUST create both a hollow enclosure body and a matching lid as
  part of one completed user action.
- **FR-003a**: System MUST represent each created enclosure set as a single
  FeaturePython-style parametric model object in the tree, with body/lid generated
  from that object's parameters during document recompute.
- **FR-004**: System MUST allow users to set and edit length, width, height, wall
  thickness, lid thickness and gap as named parameters before and after initial creation, including
  editing an existing enclosure through the model view Data section, using
  millimeters as the canonical parameter unit.
- **FR-004a**: System MUST keep lid and body outer lateral dimensions equal
  (same X/Y footprint); the `gap` parameter MUST be applied to mating clearance
  between lid and body, not by enlarging the lid outer footprint.
- **FR-005**: System MUST validate parameter values before geometry creation and
  present a clear corrective message when validation fails.
- **FR-005a**: System MUST prefill all five enclosure parameters with fixed MVP
  default values on creation while allowing user override before confirmation.
- **FR-005b**: System MUST use the following MVP defaults: length 80 mm, width 50
  mm, height 25 mm, wall thickness 2.0 mm, lid thickness to 3 mm and gap 0.20 mm.
- **FR-006**: System MUST define and document installation, update, and deployment
  steps that a new user can execute without source-level modifications.
- **FR-007**: System MUST define documented run and debug workflows for maintainers,
  including how to verify the toolbar action behavior after changes.
- **FR-008**: System MUST define a baseline architecture that explicitly maps the
  long-term automation goals from `docs/idea.md` to future feature extension points.
- **FR-009**: System MUST preserve backward compatibility for the base enclosure user
  flow when future automation capabilities are added.
- **FR-010**: System MUST create a new enclosure set on each toolbar invocation and
  ensure each created set has a unique, non-colliding identity in the document.
- **FR-011**: System MUST treat KiCad/board import, automatic screw-hole placement,
  and automatic connector/component cutout generation as out of scope for this
  feature release.
- **FR-012**: System MUST provide user-triggerable controls to toggle body and lid
  visibility independently for a selected enclosure object.

### Integration & Tooling Requirements *(mandatory)*

- **ITR-001**: The feature MUST define and expose an in-app integration point through
  a workbench and toolbar action for enclosure creation.
- **ITR-002**: The feature MUST record dependency and reuse decisions so maintainers
  can verify that reusable capabilities were evaluated before custom additions.
- **ITR-003**: The feature MUST define parameter names, units, defaults, and allowed
  ranges for length, width, height, wall thickness, lid thickness and gap, with millimeters as the
  canonical unit.
- **ITR-004**: The feature MUST define quality gates that include lint conformance,
  automated checks, and an in-app smoke path for toolbar-driven enclosure creation.

### Assumptions

- The first release focuses on manual parameter-driven enclosure creation and does
  not yet import board data directly from external design tools.
- The initial deployment target is a local user installation flow suitable for
  developer and early-user testing.
- A single default enclosure profile is sufficient for MVP, with future profiles
  added in follow-up features.
- Architecture definition is produced as part of this feature and is treated as the
  baseline for follow-up capabilities listed in `docs/idea.md`.

### Dependencies

- The project has access to a FreeCAD environment where workbench actions can be
  executed by users during acceptance testing.
- Stakeholders provide architecture review feedback against `docs/idea.md` before
  transitioning to follow-up planning.

### Key Entities *(include if feature involves data)*

- **EnclosureParameterSet**: User-controlled dimensions and tolerance inputs,
  including length, width, height, wall thickness, lid thickness, gap, unit context, and defaults.
- **EnclosureModelSet**: The resulting paired geometry outputs (body and lid) and
  their linkage to one parameter set for regeneration.
- **WorkbenchAction**: A user-invoked action exposed in the toolbar that triggers
  creation, validation, and update flow for an enclosure model set.

### Architecture Artifacts

- **Capability Map Document**: A maintained architecture document mapping current and
  future product capabilities (base box, board-driven enclosure, screw holes,
  connector cutouts) to extension boundaries in the solution, located at
  `docs/architecture/capability-map.md`.
- **Extension Boundaries Document**: Boundary contracts between command, domain, and
  integration layers for future capability additions, located at
  `docs/architecture/extension-boundaries.md`.
- **Compatibility Guarantees Document**: Backward-compatibility constraints for the
  base enclosure create/update flow, located at
  `docs/architecture/compatibility.md`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: At least 90% of test users can create a valid enclosure body and lid
  from the toolbar in under 3 minutes on first attempt.
- **SC-002**: For 100% of valid parameter updates in acceptance testing, the body and
  lid regenerate successfully without manual geometry repair.
- **SC-003**: 100% of documented installation test runs on clean environments result
  in a visible workbench and executable toolbar action.
- **SC-004**: Architecture review sign-off confirms all four long-term capabilities
  from `docs/idea.md` are mapped to extension points before planning the next phase.
