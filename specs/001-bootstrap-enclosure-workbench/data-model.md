# Data Model: Basic Workbench Scaffold

## Entity: EnclosureParameterSet

- Purpose: Holds user-editable, deterministic parameters used to generate geometry.
- Fields:
  - `id` (string): Unique identifier for one enclosure set.
  - `name` (string): Human-readable label unique within a document.
  - `length` (float): Outer length in millimeters.
  - `width` (float): Outer width in millimeters.
  - `height` (float): Outer height in millimeters.
  - `wall_thickness` (float): Wall thickness in millimeters.
  - `gap` (float): Lid/body tolerance gap in millimeters.
  - `created_at` (datetime): Creation timestamp.
  - `updated_at` (datetime): Last parameter update timestamp.
- Defaults:
  - `length=80`, `width=50`, `height=25`, `wall_thickness=2.0`, `gap=0.20`
- Validation rules:
  - Length, width, height MUST be > 0.
  - Wall thickness MUST be > 0 and less than half of min(length, width, height).
  - Gap MUST be >= 0 and <= wall thickness.

## Entity: EnclosureModelSet

- Purpose: Represents paired output models generated from one parameter set.
- Fields:
  - `id` (string): Unique identifier, matches `EnclosureParameterSet.id`.
  - `body_object_name` (string): FreeCAD document object name for hollow body.
  - `lid_object_name` (string): FreeCAD document object name for lid.
  - `document_id` (string): Owning FreeCAD document identity.
  - `status` (enum): `draft`, `valid`, `invalid`.
  - `last_regen_result` (string): Summary of last regeneration result.
- Relationships:
  - One-to-one with `EnclosureParameterSet`.
- State transitions:
  - `draft` -> `valid` after successful initial creation.
  - `valid` -> `invalid` when parameter update fails validation/regeneration.
  - `invalid` -> `valid` after corrected parameters regenerate successfully.

## Entity: WorkbenchAction

- Purpose: Defines user-invoked command metadata and behavior.
- Fields:
  - `command_id` (string): Stable identifier for toolbar action.
  - `toolbar_group` (string): Toolbar grouping label.
  - `display_name` (string): User-facing command text.
  - `enabled_state` (enum): `enabled`, `disabled` based on document context.
- Validation rules:
  - Action MUST be disabled or return a clear error when no writable document exists.

## Architecture Artifact: Capability Map

- Purpose: Design document that captures current and future capability boundaries.
- Type: Documentation artifact, not a runtime entity persisted in the FreeCAD model.
- Location: `docs/architecture/capability-map.md`
- Required contents:
  - Capability identity (`base_enclosure`, `board_import`,
    `screw_hole_automation`, `connector_cutout_automation`).
  - Delivery status (`implemented`, `planned`).
  - Integration boundary (domain/integration module where capability fits).
  - Dependency notes for later phases.
- Rules:
  - For this feature, only `base_enclosure` is `implemented`.
  - Remaining capabilities MUST be recorded as `planned`.
