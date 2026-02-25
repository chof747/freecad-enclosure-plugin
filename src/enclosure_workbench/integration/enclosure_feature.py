"""FeaturePython proxy for enclosure parametric object behavior."""

from __future__ import annotations

from pathlib import Path

from enclosure_workbench.domain.enclosure_builder import EnclosureBuilder
from enclosure_workbench.domain.parameters import (
    EnclosureParameters,
    validate_parameters,
)


ICON_PATH = (
    Path(__file__).resolve().parents[1]
    / "resources"
    / "icons"
    / "enclosure_workbench.svg"
)


def _set_if_missing(
    obj: object, prop_type: str, prop_name: str, group: str, doc: str
) -> bool:
    """Add a property only when it does not already exist."""
    if hasattr(obj, prop_name):
        return False
    obj.addProperty(prop_type, prop_name, group, doc)
    return True


class EnclosureFeatureProxy:
    """Create/update an enclosure shape from object Data properties."""

    def __init__(self, obj: object) -> None:
        """Attach parameter/display properties and register this proxy."""
        self._attach_properties(obj)
        obj.Proxy = self

    def _attach_properties(self, obj: object) -> None:
        """Ensure all expected Data properties exist on the FeaturePython object."""
        _set_if_missing(
            obj,
            "App::PropertyString",
            "EnclosureId",
            "Enclosure",
            "Stable enclosure id",
        )
        _set_if_missing(
            obj,
            "App::PropertyString",
            "BodyObjectName",
            "Enclosure",
            "Compatibility body token",
        )
        _set_if_missing(
            obj,
            "App::PropertyString",
            "LidObjectName",
            "Enclosure",
            "Compatibility lid token",
        )
        _set_if_missing(
            obj, "App::PropertyLength", "Length", "Parameters", "Outer length"
        )
        _set_if_missing(
            obj, "App::PropertyLength", "Width", "Parameters", "Outer width"
        )
        _set_if_missing(
            obj, "App::PropertyLength", "Height", "Parameters", "Outer height"
        )
        _set_if_missing(
            obj,
            "App::PropertyLength",
            "WallThickness",
            "Parameters",
            "Wall thickness",
        )
        _set_if_missing(
            obj,
            "App::PropertyLength",
            "LidThickness",
            "Parameters",
            "Lid thickness",
        )
        _set_if_missing(
            obj, "App::PropertyLength", "Gap", "Parameters", "Lid fit tolerance"
        )
        if _set_if_missing(
            obj,
            "App::PropertyBool",
            "ShowBody",
            "Display",
            "Render enclosure body",
        ):
            obj.ShowBody = True
        if _set_if_missing(
            obj,
            "App::PropertyBool",
            "ShowLid",
            "Display",
            "Render enclosure lid",
        ):
            obj.ShowLid = True

    def execute(self, fp: object) -> None:
        """Recompute enclosure geometry from Data properties during document recompute."""
        try:
            import FreeCAD as app  # type: ignore
            import Part  # type: ignore

            params = EnclosureParameters(
                length=float(fp.Length),
                width=float(fp.Width),
                height=float(fp.Height),
                wall_thickness=float(fp.WallThickness),
                lid_thickness=float(fp.LidThickness),
                gap=float(fp.Gap),
            )
            validate_parameters(params)
            geometry = EnclosureBuilder().build(params)

            body_outer = Part.makeBox(*geometry.body_outer)
            body_inner = Part.makeBox(
                *geometry.body_inner,
                app.Vector(*geometry.body_inner_offset),
            )
            body = body_outer.cut(body_inner)

            lid_outer = Part.makeBox(
                *geometry.lid_outer,
                app.Vector(*geometry.lid_offset),
            )
            lip_outer = Part.makeBox(
                *geometry.lip_outer,
                app.Vector(*geometry.lip_offset),
            )
            lip_inner = Part.makeBox(
                *geometry.lip_inner,
                app.Vector(
                    geometry.lip_offset[0]
                    + ((geometry.lip_outer[0] - geometry.lip_inner[0]) / 2.0),
                    geometry.lip_offset[1]
                    + ((geometry.lip_outer[1] - geometry.lip_inner[1]) / 2.0),
                    geometry.lip_offset[2],
                ),
            )

            lid = lid_outer.fuse(lip_outer.cut(lip_inner))

            shapes = []
            if bool(getattr(fp, "ShowBody", True)):
                shapes.append(body)
            if bool(getattr(fp, "ShowLid", True)):
                shapes.append(lid)

            if not shapes:
                fp.Shape = Part.Shape()
            elif len(shapes) == 1:
                fp.Shape = shapes[0]
            else:
                fp.Shape = Part.makeCompound(shapes)
        except Exception:
            return

    def dumps(self) -> dict[str, str]:
        """Return proxy serialization payload for FreeCAD save support."""
        return {}

    def loads(self, state: dict[str, str]) -> None:
        """Load proxy serialization payload for FreeCAD restore support."""
        return


class EnclosureViewProvider:
    """View provider used for icon assignment and proxy persistence hooks."""

    def __init__(self, vobj: object) -> None:
        """Attach this view provider proxy to the visual object."""
        vobj.Proxy = self

    def getIcon(self) -> str:
        """Return the icon path shown in the tree and workbench UI."""
        return str(ICON_PATH)

    def attach(self, _vobj: object) -> None:
        """FreeCAD callback invoked when the view provider is attached."""
        return

    def dumps(self) -> dict[str, str]:
        """Return view-provider serialization payload for save support."""
        return {}

    def loads(self, state: dict[str, str]) -> None:
        """Load view-provider serialization payload for restore support."""
        return
