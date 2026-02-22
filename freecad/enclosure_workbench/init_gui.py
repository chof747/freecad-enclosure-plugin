"""FreeCAD GUI registration for the Enclosure workbench."""

from pathlib import Path
import sys
import traceback

import FreeCAD as fc  # type: ignore
import FreeCADGui as fcg  # type: ignore

try:
    from FreeCADGui import Workbench  # type: ignore
except ImportError:
    Workbench = object


ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
ICON_PATH = (
    SRC / "enclosure_workbench" / "resources" / "icons" / "enclosure_workbench.svg"
)
TOGGLE_BODY_ICON_PATH = (
    SRC / "enclosure_workbench" / "resources" / "icons" / "toggle_body_visibility.svg"
)
TOGGLE_LID_ICON_PATH = (
    SRC / "enclosure_workbench" / "resources" / "icons" / "toggle_lid_visibility.svg"
)
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


def _print_error(message):
    try:
        fc.Console.PrintError("[enclosure_workbench] %s\n" % message)
    except Exception:
        pass


class CreateEnclosureCommand:
    def GetResources(self):  # noqa: N802
        return {
            "MenuText": "Create Enclosure",
            "ToolTip": "Create a new parametric enclosure set",
            "Pixmap": str(ICON_PATH),
        }

    def Activated(self):  # noqa: N802
        try:
            from enclosure_workbench.commands.create_enclosure import (
                create_enclosure_set,
            )

            result = create_enclosure_set()
            if not result.ok and result.error is not None:
                _print_error(result.error.message)
                return
            if result.payload is not None:
                fc.Console.PrintMessage(
                    "[enclosure_workbench] Created %s\n" % result.payload["name"]
                )
        except Exception as exc:
            _print_error("CreateEnclosure failed: %s" % exc)
            _print_error(traceback.format_exc())

    def IsActive(self):  # noqa: N802
        return True


def _selected_enclosure_id() -> str | None:
    selection = fcg.Selection.getSelection()
    if len(selection) != 1:
        return None
    obj = selection[0]
    enclosure_id = getattr(obj, "EnclosureId", "")
    return str(enclosure_id) if enclosure_id else None


class ToggleEnclosurePartCommand:
    def __init__(self, target: str, menu_text: str, tooltip: str, pixmap: str) -> None:
        self._target = target
        self._menu_text = menu_text
        self._tooltip = tooltip
        self._pixmap = pixmap

    def GetResources(self):  # noqa: N802
        return {
            "MenuText": self._menu_text,
            "ToolTip": self._tooltip,
            "Pixmap": self._pixmap,
        }

    def Activated(self):  # noqa: N802
        enclosure_id = _selected_enclosure_id()
        if not enclosure_id:
            _print_error("Select one enclosure object first")
            return

        try:
            from enclosure_workbench.commands.toggle_enclosure_visibility import (
                toggle_enclosure_visibility,
            )

            result = toggle_enclosure_visibility(enclosure_id, self._target)
            if not result.ok and result.error is not None:
                _print_error(result.error.message)
        except Exception as exc:
            _print_error("Toggle visibility failed: %s" % exc)
            _print_error(traceback.format_exc())

    def IsActive(self):  # noqa: N802
        return _selected_enclosure_id() is not None


class EnclosureWorkbench(Workbench):
    MenuText = "Enclosure"
    ToolTip = "Create and update parametric enclosure sets"
    Icon = str(ICON_PATH)

    def GetClassName(self):  # noqa: N802
        return "Gui::PythonWorkbench"

    def Initialize(self):  # noqa: N802
        try:
            fcg.addCommand("CreateEnclosure", CreateEnclosureCommand())
            fcg.addCommand(
                "ToggleEnclosureBody",
                ToggleEnclosurePartCommand(
                    target="body",
                    menu_text="Toggle Enclosure Body",
                    tooltip="Toggle body visibility for selected enclosure",
                    pixmap=str(TOGGLE_BODY_ICON_PATH),
                ),
            )
            fcg.addCommand(
                "ToggleEnclosureLid",
                ToggleEnclosurePartCommand(
                    target="lid",
                    menu_text="Toggle Enclosure Lid",
                    tooltip="Toggle lid visibility for selected enclosure",
                    pixmap=str(TOGGLE_LID_ICON_PATH),
                ),
            )
            command_ids = [
                "CreateEnclosure",
                "ToggleEnclosureBody",
                "ToggleEnclosureLid",
            ]
            self.appendToolbar("Enclosure", command_ids)
            self.appendMenu("Enclosure", command_ids)
        except Exception as exc:
            _print_error("Workbench initialization failed: %s" % exc)
            _print_error(traceback.format_exc())


def register_workbench():
    try:
        fcg.addWorkbench(EnclosureWorkbench())
    except KeyError:
        # FreeCAD may import both legacy and modern init modules.
        # Ignore duplicate registration for the same class name.
        pass
    except Exception as exc:
        _print_error("Workbench registration failed: %s" % exc)
        _print_error(traceback.format_exc())


register_workbench()
