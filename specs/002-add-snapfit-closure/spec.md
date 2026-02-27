# Feature Specification: Snap-Fit Closing Mechanism

**Feature Branch**: `002-add-snapfit-closure`  
**Created**: 2026-02-25  
**Status**: Draft  
**Input**: User description: "snapfit closing mechanisms: We want to add a (later more) closing mechanisms to the enclosure model that allows a snap-fit connection between the body and the lid. The snap fit connection should be printable and reversible (so that the enclosure could be opened again). The parameters for the snap fit should be added with suitable default values to the enclosure model together with an enum to decide on the concrete closing mechism (at the moment: None and Snap-Fit)"

## Clarifications

### Session 2026-02-25

- Q: What should happen when `snap_fit` is selected but parameters or dimensions are invalid? → A: Auto-clamp parameters to nearest valid values and continue generation with a warning.
- Q: What should happen when enclosure dimensions are too small for any valid `snap_fit` even after clamping? → A: Stop generation for `snap_fit` and show an explicit error.
- Q: What should happen to custom `snap_fit` parameters when switching closing mechanism to `none`? → A: Preserve custom values and restore them when `snap_fit` is reselected.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Enable snap-fit closure (Priority: P1)

As a designer, I can select the `snap_fit` closing mechanism (displayed as "Snap-Fit") so the generated enclosure body and lid can lock together without separate fasteners.

**Why this priority**: This is the core value of the feature and the primary new capability users requested.

**Independent Test**: Can be fully tested by creating an enclosure with the closing mechanism set to `snap_fit` and verifying that the body and lid include matching, printable, reversible snap-fit features that assemble and disassemble without permanent damage.

**Acceptance Scenarios**:

1. **Given** an enclosure model with closing mechanism set to `snap_fit`, **When** the model is generated, **Then** both body and lid include matching snap-fit features designed to engage with each other.
2. **Given** an enclosure model with closing mechanism set to `snap_fit`, **When** a user assembles and then opens the enclosure, **Then** the connection can be reversed without requiring destructive removal.

---

### User Story 2 - Keep closures optional (Priority: P2)

As a designer, I can choose the `none` closing mechanism (displayed as "None") so existing open-fit workflows remain available.

**Why this priority**: Backward-compatible behavior is critical so current designs are not forced into snap-fit use.

**Independent Test**: Can be fully tested by generating an enclosure with closing mechanism set to `none` and verifying no snap-fit closure features are created.

**Acceptance Scenarios**:

1. **Given** an enclosure model with closing mechanism set to `none`, **When** the model is generated, **Then** no snap-fit closure geometry is added to body or lid.

---

### User Story 3 - Adjust snap-fit behavior with defaults (Priority: P3)

As a designer, I can review and adjust snap-fit parameters, starting from sensible defaults, to match print tolerances and use cases.

**Why this priority**: Parameter control is needed for practical printability across different printers and materials.

**Independent Test**: Can be fully tested by creating an enclosure with default snap-fit parameters, then changing one parameter and confirming the generated snap-fit geometry updates accordingly while remaining valid.

**Acceptance Scenarios**:

1. **Given** an enclosure model with `snap_fit` selected, **When** the model is initialized, **Then** snap-fit parameters are present with predefined default values.
2. **Given** an enclosure model with `snap_fit` selected, **When** a user changes one or more snap-fit parameters, **Then** the generated closure geometry reflects the updated values.

### Edge Cases

- Very small enclosure dimensions that cannot host default snap-fit geometry trigger parameter clamping first; if no valid geometry remains, `snap_fit` generation is blocked and users receive a clear dimensional error.
- Invalid Snap-Fit parameter values are automatically clamped to the nearest valid range, model generation continues, and users receive a warning describing what was adjusted.
- Switching from `snap_fit` to `none` suppresses snap-fit geometry but preserves custom snap-fit parameter values for reuse if `snap_fit` is selected again.
- Wall and tolerance combinations that leave insufficient reversible-opening clearance are treated as invalid Snap-Fit conditions: parameters are clamped when possible, otherwise generation is blocked with an explicit error.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The enclosure model MUST provide a closing mechanism selection with at least canonical values `none` and `snap_fit` (display labels "None" and "Snap-Fit").
- **FR-002**: When closing mechanism is set to `snap_fit`, the system MUST generate matching closure features on body and lid that engage as a snap-fit pair.
- **FR-003**: Snap-fit closure geometry MUST be reversible, allowing the enclosure to be opened again without destructive removal in normal use.
- **FR-004**: The enclosure model MUST expose snap-fit configuration parameters with explicit defaults: `tab_count=2`, `tab_length_mm=10.0`, `tab_width_mm=5.0`, `tab_thickness_mm=1.8`, `undercut_mm=0.6`, `lead_in_angle_deg=35.0`, `retention_angle_deg=10.0`, and `clearance_mm=0.20`.
- **FR-005**: The system MUST allow users to modify snap-fit parameter values and regenerate closure geometry using those values.
- **FR-006**: When closing mechanism is set to `none`, the system MUST omit snap-fit closure geometry from the body and lid.
- **FR-007**: If snap-fit parameters are outside valid ranges, the system MUST clamp them to the nearest valid values, continue generation, and surface clear warning feedback describing each applied adjustment.
- **FR-008**: Existing enclosure configurations that do not explicitly set a closing mechanism MUST continue to generate successfully with behavior equivalent to `none`.
- **FR-009**: If enclosure dimensions cannot support any valid snap-fit geometry even after parameter clamping, the system MUST stop `snap_fit` generation and present a clear error indicating the dimensional constraint.
- **FR-010**: When users switch the closing mechanism from `snap_fit` to `none`, the system MUST preserve the most recent snap-fit parameter values and restore them if `snap_fit` is selected again.

### Documentation & Maintainability Requirements

- **DMR-001**: Code introduced or modified by this feature MUST include docstrings for classes, methods, and functions.
- **DMR-002**: User-facing parameter descriptions for closing mechanism and snap-fit settings MUST explain intended effect in plain language.

### Key Entities *(include if feature involves data)*

- **Closing Mechanism Setting**: User-selectable enclosure closure mode; includes canonical values (`none`, `snap_fit`) with display labels ("None", "Snap-Fit") and determines whether closure geometry is generated.
- **Snap-Fit Parameter Set**: Collection of user-adjustable closure values with defaults that govern snap-fit behavior, geometry proportion, and assembly/disassembly clearance.
- **Closure Validation Result**: Outcome object describing whether selected mechanism and parameters can produce valid, printable, reversible closure geometry, including user-readable messages when invalid.

## Assumptions

- Snap-fit support in this feature is limited to a single snap-fit style, while the mechanism selection is intentionally extensible for future closure types.
- "Printable" means the generated closure geometry can be produced with common enclosure 3D-printing workflows without requiring non-standard post-processing.
- "Reversible" means users can open and close the enclosure repeatedly under normal handling; extreme force and material fatigue are outside the feature guarantee.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of new enclosure models show a closing mechanism selection that includes canonical values `none` and `snap_fit`.
- **SC-002**: In validation tests using default settings across a representative set of enclosure sizes, at least 95% of generated Snap-Fit models produce valid body/lid closure geometry without manual parameter changes.
- **SC-003**: In user acceptance testing, at least 90% of participants can configure an enclosure for Snap-Fit and regenerate the model in under 2 minutes on their first attempt.
- **SC-004**: In bench testing of generated sample models, at least 95% of Snap-Fit closures can be assembled and reopened at least 5 times without permanent closure failure.
