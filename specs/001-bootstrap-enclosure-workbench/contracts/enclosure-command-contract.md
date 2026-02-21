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
- `gap`

Unit for all parameter values is millimeters.

## Command: create_enclosure_set

- Input:
  - `name` (optional string)
  - `parameters` (object)
    - `length` (float, default 80)
    - `width` (float, default 50)
    - `height` (float, default 25)
    - `wall_thickness` (float, default 2.0)
    - `gap` (float, default 0.20)
- Behavior:
  - Creates one new enclosure set each invocation.
  - Creates body + lid pair with unique non-colliding identity in document.
  - Returns validation error if parameters are invalid.
- Output:
  - `id` (string)
  - `name` (string)
  - `parameters` (object)
  - `body_object_name` (string)
  - `lid_object_name` (string)
  - `status` (`draft` | `valid` | `invalid`)

## Command: update_enclosure_set

- Input:
  - `id` (string, required)
  - `parameters` (partial object; same canonical names)
- Behavior:
  - Updates the target enclosure parameter properties in model Data section.
  - Regenerates body + lid deterministically for valid values.
  - Returns not-found error when `id` does not exist.
  - Returns validation error when values violate rules.
- Trigger semantics:
  - In toolbar/macro usage, this command is called explicitly by the caller.
  - In model-view editing, this command is called by the feature-object update hook
    when a parameter value is committed and the document recomputes.
  - It is not called on every keystroke while typing in the property editor.
- Output:
  - Updated enclosure set payload with same fields as create output.

## Validation Rules

- `length > 0`
- `width > 0`
- `height > 0`
- `wall_thickness > 0`
- `wall_thickness < min(length, width, height) / 2`
- `gap >= 0`
- `gap <= wall_thickness`

## Error Shape

- `code` (string)
- `message` (string)
