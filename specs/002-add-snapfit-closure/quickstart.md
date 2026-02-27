# Quickstart - Snap-Fit Closing Mechanism

## 1) Prepare environment

```bash
uv sync
```

## 2) Run automated checks

```bash
uv run flake8
uv run pytest tests/unit tests/contract tests/integration
```

## 3) Validate command contract behavior

1. Create enclosure with default parameters and verify payload includes `closing_mechanism` with default behavior equivalent to `none`.
2. Update enclosure to `closing_mechanism = snap_fit` and verify snap-fit defaults are present.
3. Submit out-of-range snap-fit values and verify:
   - values are clamped to nearest valid bounds,
   - warnings are returned with input and applied values,
   - payload status reflects warning state.
4. Submit dimensions that cannot support any snap-fit after clamping and verify command returns `validation_error`.
5. Switch mechanism from `snap_fit` to `none`, then back to `snap_fit`, and verify previous snap-fit values are restored.

## 4) FreeCAD smoke run

1. Launch FreeCAD with plugin enabled.
2. Open Enclosure workbench and run `Create Enclosure` command.
3. Confirm enclosure body and lid are created.
4. Apply parameter updates through command path and verify:
   - `none` mode creates no snap-fit geometry,
   - `snap_fit` mode creates matching closure features,
   - invalid snap-fit cases emit warnings/errors per contract.

## 5) Done criteria for this feature slice

- All tests pass with `uv run` commands.
- FreeCAD smoke path succeeds without runtime exceptions.
- Contract responses include warning/error semantics for clamp and hard-fail scenarios.
