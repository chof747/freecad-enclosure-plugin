# Quickstart: Basic Workbench Scaffold

## Prerequisites

- FreeCAD installed and launchable.
- `uv` installed.
- Repository cloned locally.

## 1) Install project dependencies

```bash
uv sync
```

## 2) Run quality checks

```bash
uv run flake8
uv run pytest tests/unit
```

## 3) Run integration checks

```bash
uv run pytest tests/integration
uv run pytest tests/contract
```

## 4) Local installation into FreeCAD user mod path

1. Use helper install script or copy/symlink manually to FreeCAD `Mod` directory.
   - Linux: `scripts/install-local.sh "$HOME/.local/share/FreeCAD/Mod/enclosure_workbench"`
   - macOS: `scripts/install-local.sh "$HOME/Library/Application Support/FreeCAD/Mod/enclosure_workbench"`
   - Windows: pass `%APPDATA%/FreeCAD/Mod/enclosure_workbench` path to script.
2. Restart FreeCAD.
3. Enable/select the enclosure workbench.

### Update flow

- Pull latest code with `scripts/update-local.sh`.
- Restart FreeCAD to load updates.

## 5) Smoke validation in FreeCAD

1. Open or create a new writable document.
2. Trigger toolbar action: `Create Enclosure` (calls `create_enclosure_set`).
3. Confirm default values are prefilled:
   - Length: 80 mm
   - Width: 50 mm
   - Height: 25 mm
   - Wall thickness: 2.0 mm
   - Gap: 0.20 mm
4. Confirm one body and one lid are created.
5. Edit parameters in the model view Data section and recompute
   (calls `update_enclosure_set`).
6. Select an enclosure object and use `Toggle Enclosure Body` /
   `Toggle Enclosure Lid` to control visibility.
7. Trigger action again and confirm a new uniquely named enclosure set is created.

## 6) Macro/scripting entrypoints

- `create_enclosure_set(name=None, parameters=None)`
- `update_enclosure_set(id, parameters)`
- `toggle_enclosure_visibility(id, target)` where `target` is `"body"`, `"lid"`, or `"both"`

Example:

```python
create_enclosure_set(parameters={"length": 80, "width": 50, "height": 25, "wall_thickness": 2.0, "gap": 0.20})
update_enclosure_set(id="enclosure_001", parameters={"gap": 0.25})
toggle_enclosure_visibility("enclosure_001", "lid")
```

## 7) Debug workflow

- Attach VS Code to a running FreeCAD process with `debugpy`:

1. Start FreeCAD and open the Python console.
2. Run:

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
print("debugpy listening on 5678")
```

3. In VS Code, select and start `Attach to FreeCAD (debugpy:5678)` from
   `.vscode/launch.json`.
4. Trigger `Create Enclosure` or edit Data parameters, then hit breakpoints.

- Run focused tests while iterating:

```bash
uv run pytest tests/unit/test_parameters.py -q
uv run pytest tests/integration/test_create_enclosure_set_command.py -q
uv run pytest tests/contract/test_create_enclosure_set_contract.py -q
uv run pytest tests/contract/test_update_enclosure_set_contract.py -q
```

- Re-run `uv run flake8` before merge.

## 8) Architecture traceability checks

- Confirm capability status map: `docs/architecture/capability-map.md`
- Confirm extension boundaries: `docs/architecture/extension-boundaries.md`
- Confirm compatibility guarantees: `docs/architecture/compatibility.md`

## Validation Notes

- Automated validation run completed with `uv run flake8 .` and `uv run pytest`.
- Current baseline result: lint pass, `14 passed` tests.
