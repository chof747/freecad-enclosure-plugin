# Data Model - Snap-Fit Closing Mechanism

## Entity: EnclosureConfig

- **Purpose**: Canonical user-configurable enclosure parameter set used by create/update command flows.
- **Fields**:
  - `id` (string, immutable identifier)
  - `name` (string, user-visible label)
  - `base_dimensions` (object)
    - `length_mm` (number, > 0)
    - `width_mm` (number, > 0)
    - `height_mm` (number, > 0)
  - `wall_thickness_mm` (number, > 0 and < half of min dimension)
  - `lid_thickness_mm` (number, > 0)
  - `gap_mm` (number, >= 0 and <= wall thickness)
  - `closing_mechanism` (enum: `none`, `snap_fit`)
  - `snap_fit` (SnapFitConfig, present when mechanism is `snap_fit`, preserved otherwise)
  - `status` (enum: `valid`, `warning`, `error`)

## Entity: SnapFitConfig

- **Purpose**: Parameter set controlling snap-fit geometry generation.
- **Fields**:
  - `version` (integer, starts at 1)
  - `tab_count` (integer, default 2, valid range 1-8)
  - `tab_length_mm` (number, default 10.0, bounded)
  - `tab_width_mm` (number, default 5.0, bounded)
  - `tab_thickness_mm` (number, default 1.8, bounded)
  - `undercut_mm` (number, default 0.6, bounded)
  - `lead_in_angle_deg` (number, default 35.0, bounded)
  - `retention_angle_deg` (number, default 10.0, bounded)
  - `clearance_mm` (number, default 0.2, bounded)
  - `warnings` (list of ValidationWarning entries from clamped values)

## Entity: ValidationWarning

- **Purpose**: Captures non-blocking automatic parameter corrections.
- **Fields**:
  - `code` (string, stable warning identifier)
  - `parameter` (string, canonical parameter key)
  - `input_value` (number)
  - `applied_value` (number)
  - `message` (string, user-readable adjustment explanation)

## Entity: ValidationError

- **Purpose**: Captures blocking validation outcomes.
- **Fields**:
  - `code` (string, stable error identifier)
  - `message` (string, user-readable explanation)
  - `context` (object, optional dimensions/parameters causing block)

## Relationships

- `EnclosureConfig.closing_mechanism = snap_fit` activates `SnapFitConfig` for geometry generation.
- `EnclosureConfig.closing_mechanism = none` omits snap-fit geometry but does not erase stored `SnapFitConfig`.
- Validation outcomes (`ValidationWarning`, `ValidationError`) are produced from `EnclosureConfig` + `SnapFitConfig` evaluation.

## State Transitions

- `Draft input` -> `Validated` when base + mechanism parameters are checked.
- `Validated` -> `Warning` when one or more snap-fit fields are clamped.
- `Validated/Warning` -> `Error` when no valid snap-fit geometry can be produced after clamping.
- `snap_fit` -> `none` preserves snap-fit parameters and suppresses snap-fit geometry.
- `none` -> `snap_fit` restores preserved snap-fit parameters (or defaults when none exist yet).

## Validation Rules Snapshot

- Base enclosure parameter rules remain unchanged and continue to block on invalid dimensions.
- Snap-fit parameter rules are bounded and clamp to nearest valid values where safe.
- Generation blocks when dimensional constraints cannot satisfy printable/reversible snap-fit geometry even after clamping.
- Validation messages distinguish warning (auto-adjusted) from error (generation blocked).
