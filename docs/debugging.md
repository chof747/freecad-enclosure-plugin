# Debugging

## Attach debugpy from FreeCAD

1. Open FreeCAD Python console.
2. Run:

```python
import debugpy
debugpy.listen(("127.0.0.1", 5678))
print("debugpy listening on 5678")
```

3. In VS Code, run `Attach to FreeCAD (debugpy:5678)` from `.vscode/launch.json`.
4. Trigger `Create Enclosure` and debug command execution.
