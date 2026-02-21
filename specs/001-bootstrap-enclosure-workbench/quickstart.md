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

1. Copy or symlink this repository to your FreeCAD `Mod` directory:
   - Linux: `~/.local/share/FreeCAD/Mod/`
   - macOS: `~/Library/Preferences/FreeCAD/Mod/`
   - Windows: `%APPDATA%\\FreeCAD\\Mod\\`
2. Restart FreeCAD.
3. Enable/select the enclosure workbench.

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
6. Trigger action again and confirm a new uniquely named enclosure set is created.

## 6) Macro/scripting entrypoints

- `create_enclosure_set(name=None, parameters=None)`
- `update_enclosure_set(id, parameters)`

Example:

```python
create_enclosure_set(parameters={"length": 80, "width": 50, "height": 25, "wall_thickness": 2.0, "gap": 0.20})
update_enclosure_set(id="enclosure_001", parameters={"gap": 0.25})
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
