# Installation

## Local setup

1. Install dependencies:
   - `uv sync --extra dev`
2. Link plugin into FreeCAD Mod path:
   - macOS: `scripts/install-local.sh "$HOME/Library/Application Support/FreeCAD/Mod/enclosure_workbench"`
   - Linux: `scripts/install-local.sh "$HOME/.local/share/FreeCAD/Mod/enclosure_workbench"`
   - Windows (WSL/Git Bash): pass `%APPDATA%/FreeCAD/Mod/enclosure_workbench`
3. Restart FreeCAD and select the Enclosure workbench.

## Update

1. Pull latest changes: `scripts/update-local.sh`
2. Restart FreeCAD.
