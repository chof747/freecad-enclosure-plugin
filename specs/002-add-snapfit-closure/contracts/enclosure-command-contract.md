# Enclosure Command Contract

## Purpose

This is an in-process contract for the FreeCAD workbench command layer. It is not an
HTTP API. The same contract is used by:

- toolbar command execution,
- Python scripting/macros inside FreeCAD,
- contract tests in `tests/contract/`.

## Canonical Parameter Names

- `length`
- `width`
- `height`
- `wall_thickness`
- `lid_thickness`
- `gap`
- `closing_mechanism`
- `snap_fit`

Unit for all numeric parameter values is millimeters unless noted.

## Command: create_enclosure_set

- Input:
  - `name` (optional string)
  - `parameters` (object)
    - `length` (float, default 80)
    - `width` (float, default 50)
    - `height` (float, default 25)
    - `wall_thickness` (float, default 2.0)
    - `lid_thickness` (float, default 3.0)
    - `gap` (float, default 0.20)
    - `closing_mechanism` (`none` | `snap_fit`, default `none`)
    - `snap_fit` (object, optional; ignored for geometry when mechanism is `none`)
      - `tab_count` (int, default 2)
      - `tab_length_mm` (float, default 10.0)
      - `tab_width_mm` (float, default 5.0)
      - `tab_thickness_mm` (float, default 1.8)
      - `undercut_mm` (float, default 0.6)
      - `lead_in_angle_deg` (float, default 35.0)
      - `retention_angle_deg` (float, default 10.0)
      - `clearance_mm` (float, default 0.20)
- Behavior:
  - Creates one new enclosure set each invocation.
  - Creates body + lid pair with unique non-colliding identity in document.
  - Applies clamp-to-valid-range for safe snap-fit parameter corrections and returns
    warnings describing each adjusted value.
  - Returns validation error when no valid snap-fit geometry is possible after
    clamping.
- Output:
  - `id` (string)
  - `name` (string)
  - `parameters` (object)
  - `body_object_name` (string)
  - `lid_object_name` (string)
  - `status` (`valid` | `warning`)
  - `warnings` (array, optional; see Warning Shape)

## Command: update_enclosure_set

- Input:
  - `id` (string, required)
  - `parameters` (partial object; same canonical names)
- Behavior:
  - Updates the target enclosure parameter properties in model Data section.
  - Regenerates body + lid deterministically for valid values.
  - Returns not-found error when `id` does not exist.
  - Applies snap-fit clamps with warning feedback for safe corrections.
  - Returns validation error for blocking constraints (for example, dimensions too
    small for any valid snap-fit after clamping).
  - Switching `closing_mechanism` from `snap_fit` to `none` suppresses snap-fit
    geometry while preserving last snap-fit values for restore when `snap_fit` is
    selected again.
- Trigger semantics:
  - In toolbar/macro usage, this command is called explicitly by the caller.
  - In model-view editing, this command is called by the feature-object update hook
    when a parameter value is committed and the document recomputes.
  - It is not called on every keystroke while typing in the property editor.
- Output:
  - Updated enclosure set payload with same fields as create output.

## Validation Rules

- Base enclosure rules:
  - `length > 0`
  - `width > 0`
  - `height > 0`
  - `wall_thickness > 0`
  - `wall_thickness < min(length, width, height) / 2`
  - `gap >= 0`
  - `gap <= wall_thickness`
- Closing mechanism rules:
  - `closing_mechanism` must be one of `none` or `snap_fit`.
  - Missing `closing_mechanism` is treated as `none` for backward compatibility.
- Snap-fit rules:
  - Out-of-range tunable values are clamped to nearest valid value and added to
    warning output.
  - If constraints remain unsatisfied after clamping, generation fails with
    `validation_error`.

## Warning Shape

- `code` (string)
- `parameter` (string)
- `input_value` (number)
- `applied_value` (number)
- `message` (string)

## Error Shape

- `code` (string)
- `message` (string)
