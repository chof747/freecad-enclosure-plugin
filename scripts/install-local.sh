#!/usr/bin/env bash
set -euo pipefail

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
if [ "$#" -ge 1 ]; then
  TARGET_DIR="$1"
else
  TARGET_DIR="$HOME/Library/Application Support/FreeCAD/Mod/enclosure_workbench"
fi

mkdir -p "$(dirname "$TARGET_DIR")"
rm -rf "$TARGET_DIR"
ln -s "$PLUGIN_ROOT" "$TARGET_DIR"

printf 'Installed symlink: %s -> %s\n' "$TARGET_DIR" "$PLUGIN_ROOT"
