# FreeCAD Enclosure Plugin

Scaffold for a FreeCAD workbench that creates and updates a parametric enclosure set.

Architecture and code component overview:

- `docs/solution-architecture.md`

## Development

Install dependencies:

```bash
uv sync --extra dev
```

Run lint and tests:

```bash
uv run flake8 .
uv run pytest
```

Focused shortcuts:

```bash
uv run pytest tests/unit -q
uv run pytest tests/integration -q
uv run pytest tests/contract -q
```

Latest local execution:

- `uv run flake8 .` -> pass
- `uv run pytest` -> `14 passed`
