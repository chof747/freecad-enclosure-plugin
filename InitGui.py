"""Compatibility GUI entrypoint for FreeCAD legacy addon loading."""

try:
    from freecad.enclosure_workbench import init_gui as _init_gui

    _init_gui.register_workbench()
except Exception as exc:
    try:
        import FreeCAD as App  # type: ignore

        App.Console.PrintError("[enclosure_workbench] InitGui load failed: %s\n" % exc)
    except Exception:
        pass
