# Deployment

## Artifact

- The repository root is the deployable workbench artifact.
- Required files: `Init.py`, `InitGui.py`, `package.xml`, `src/enclosure_workbench/`.

## Release flow

1. Run quality checks:
   - `uv run flake8 .`
   - `uv run pytest`
2. Package by archiving repository contents for distribution.
3. Publish release notes with known limitations.
