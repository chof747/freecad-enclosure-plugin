# Compatibility Guarantees

- `create_enclosure_set(name=None, parameters=None)` remains callable from toolbar and macros.
- `update_enclosure_set(id, parameters)` remains explicit and deterministic.
- Canonical parameter names (`length`, `width`, `height`, `wall_thickness`, `gap`) remain stable.
- Output includes `id`, `name`, `parameters`, `body_object_name`, `lid_object_name`, `status`.
- Future capabilities must not break base enclosure create/update flow.
