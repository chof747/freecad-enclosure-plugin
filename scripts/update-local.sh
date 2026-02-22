#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if ! command -v git >/dev/null 2>&1; then
  printf 'git is required\n' >&2
  exit 1
fi

git -C "$REPO_ROOT" pull --ff-only
printf 'Repository updated at %s\n' "$REPO_ROOT"
