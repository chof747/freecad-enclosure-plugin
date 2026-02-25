"""Workbench registration and command wiring."""

from __future__ import annotations

import traceback


def _print_error(message: str) -> None:
    try:
        import FreeCAD  # type: ignore

        FreeCAD.Console.PrintError(f"[enclosure_workbench] {message}\n")
    except Exception:
        pass


try:
    BaseWorkbench = Workbench  # type: ignore[name-defined]
except NameError:
    BaseWorkbench = object


class EnclosureWorkbench(BaseWorkbench):  # type: ignore[misc,valid-type]
    MenuText = "Enclosure"
    ToolTip = "Create and update parametric enclosure sets"
    Icon = ""

    def GetClassName(self) -> str:  # noqa: N802 - FreeCAD naming
        return "Gui::PythonWorkbench"

    def Initialize(self) -> None:  # noqa: N802 - FreeCAD naming
        try:
            import FreeCADGui  # type: ignore

            FreeCADGui.addCommand("CreateEnclosure", CreateEnclosureCommand())
            if hasattr(self, "appendToolbar"):
                self.appendToolbar("Enclosure", ["CreateEnclosure"])
            if hasattr(self, "appendMenu"):
                self.appendMenu("Enclosure", ["CreateEnclosure"])
        except Exception as exc:
            _print_error(f"Workbench initialization failed: {exc}")
            _print_error(traceback.format_exc())


class CreateEnclosureCommand:
    def GetResources(self) -> dict[str, str]:  # noqa: N802 - FreeCAD naming
        return {
            "MenuText": "Create Enclosure",
            "ToolTip": "Create a new parametric enclosure set",
            "Pixmap": "",
        }

    def Activated(self) -> None:  # noqa: N802 - FreeCAD naming
        try:
            from enclosure_workbench.commands.create_enclosure import (
                create_enclosure_set,
            )

            result = create_enclosure_set()
            if not result.ok and result.error is not None:
                _print_error(result.error.message)
        except Exception as exc:
            _print_error(f"CreateEnclosure failed: {exc}")
            _print_error(traceback.format_exc())

    def IsActive(self) -> bool:  # noqa: N802 - FreeCAD naming
        return True
