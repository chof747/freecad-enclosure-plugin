#!/usr/bin/env bash
set -euo pipefail

if ! command -v freecad >/dev/null 2>&1; then
  printf 'freecad executable not found in PATH\n' >&2
  exit 1
fi

freecad --version
printf 'FreeCAD smoke check passed\n'
