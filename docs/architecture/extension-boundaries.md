# Extension Boundaries

## Domain boundary

- `src/enclosure_workbench/domain/` owns parameter validation and geometry rules.
- Future board-driven automation must plug into domain services without mutating command API shape.

## Integration boundary

- `src/enclosure_workbench/integration/` owns FreeCAD object/document adapter logic.
- Board import integrations should be added here and consumed by domain services.

## Command boundary

- `src/enclosure_workbench/commands/` exposes `create_enclosure_set` and `update_enclosure_set`.
- Existing payload and error shape are compatibility contracts.
