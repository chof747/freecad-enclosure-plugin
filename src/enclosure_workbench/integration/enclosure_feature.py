"""FeaturePython proxy for enclosure parametric object behavior."""

from __future__ import annotations

from pathlib import Path

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
    if hasattr(obj, prop_name):
        return False
    obj.addProperty(prop_type, prop_name, group, doc)
    return True


class EnclosureFeatureProxy:
    """Create/update an enclosure shape from object Data properties."""

    def __init__(self, obj: object) -> None:
        self._attach_properties(obj)
        obj.Proxy = self

    def _attach_properties(self, obj: object) -> None:
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
        try:
            import FreeCAD as app  # type: ignore
            import Part  # type: ignore

            params = EnclosureParameters(
                length=float(fp.Length),
                width=float(fp.Width),
                height=float(fp.Height),
                wall_thickness=float(fp.WallThickness),
                gap=float(fp.Gap),
            )
            validate_parameters(params)

            body_outer = Part.makeBox(params.length, params.width, params.height)
            body_inner = Part.makeBox(
                params.length - (2 * params.wall_thickness),
                params.width - (2 * params.wall_thickness),
                params.height - params.wall_thickness,
                app.Vector(
                    params.wall_thickness, params.wall_thickness, params.wall_thickness
                ),
            )
            body = body_outer.cut(body_inner)

            lid_height = max(params.wall_thickness * 2.0, params.height * 0.2)
            lip_height = max(params.wall_thickness, lid_height * 0.6)
            lip_thickness = max(params.wall_thickness * 0.5, 0.6)

            lid_outer = Part.makeBox(
                params.length,
                params.width,
                lid_height,
                app.Vector(0, 0, params.height + params.gap),
            )

            lip_outer_length = (
                params.length - (2 * params.wall_thickness) - (2 * params.gap)
            )
            lip_outer_width = (
                params.width - (2 * params.wall_thickness) - (2 * params.gap)
            )
            lip_outer = Part.makeBox(
                lip_outer_length,
                lip_outer_width,
                lip_height,
                app.Vector(
                    params.wall_thickness + params.gap,
                    params.wall_thickness + params.gap,
                    params.height + params.gap - lip_height,
                ),
            )

            lip_inner_length = max(lip_outer_length - (2 * lip_thickness), 0.1)
            lip_inner_width = max(lip_outer_width - (2 * lip_thickness), 0.1)
            lip_inner = Part.makeBox(
                lip_inner_length,
                lip_inner_width,
                lip_height,
                app.Vector(
                    params.wall_thickness + params.gap + lip_thickness,
                    params.wall_thickness + params.gap + lip_thickness,
                    params.height + params.gap - lip_height,
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
        return {}

    def loads(self, state: dict[str, str]) -> None:
        return


class EnclosureViewProvider:
    def __init__(self, vobj: object) -> None:
        vobj.Proxy = self

    def getIcon(self) -> str:
        return str(ICON_PATH)

    def attach(self, _vobj: object) -> None:
        return

    def dumps(self) -> dict[str, str]:
        return {}

    def loads(self, state: dict[str, str]) -> None:
        return
