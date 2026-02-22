"""Real FreeCAD document adapter (GUI/runtime path)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from enclosure_workbench.domain.enclosure_builder import EnclosureGeometry
from enclosure_workbench.domain.parameters import EnclosureParameters
from enclosure_workbench.integration.enclosure_feature import (
    EnclosureFeatureProxy,
    EnclosureViewProvider,
)
from enclosure_workbench.integration.enclosure_record import EnclosureRecord


PARAMETER_PROPERTY_MAP = {
    "Length": "length",
    "Width": "width",
    "Height": "height",
    "WallThickness": "wall_thickness",
    "LidThickness": "lid_thickness",
    "Gap": "gap",
}


class FreeCADDocumentAdapter:
    """Adapter that maps command operations to real FreeCAD document objects."""

    def __init__(self, writable: bool = True) -> None:
        """Capture FreeCAD application/document handles for runtime operations."""
        self._writable = writable
        self._app = None
        self._doc = None
        try:
            import FreeCAD as app  # type: ignore

            self._app = app
            self._doc = getattr(app, "ActiveDocument", None)
        except Exception:
            self._app = None
            self._doc = None

    def is_writable(self) -> bool:
        """Return True when a writable adapter and active document are available."""
        return bool(self._writable and self._doc is not None)

    def add_enclosure(
        self,
        enclosure_id: str,
        name: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord:
        """Create a new FeaturePython enclosure object and return its record."""
        feature = self._create_feature_object(name, enclosure_id, parameters)
        now = datetime.now(timezone.utc)
        return EnclosureRecord(
            id=enclosure_id,
            name=name,
            parameters=parameters,
            body_object_name=f"{feature.Name}_body",
            lid_object_name=f"{feature.Name}_lid",
            geometry=geometry,
            status="valid",
            created_at=now,
            updated_at=now,
            container_object_name=feature.Name,
        )

    def update_enclosure(
        self,
        enclosure_id: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord:
        """Update one enclosure FeaturePython object by id and recompute."""
        doc = self._require_doc()
        feature = self._find_feature_by_id(enclosure_id)
        if feature is None:
            raise KeyError(enclosure_id)

        self._set_feature_parameters(feature, parameters)
        doc.recompute()

        updated = self.get_enclosure(enclosure_id)
        if updated is None:
            raise KeyError(enclosure_id)
        updated.geometry = geometry
        return updated

    def get_enclosure(self, enclosure_id: str) -> EnclosureRecord | None:
        """Resolve an enclosure record from its FeaturePython object state."""
        feature = self._find_feature_by_id(enclosure_id)
        if feature is None:
            return None

        parameters = self._parameters_from_feature(feature)
        shape = getattr(feature, "Shape", None)
        solids = getattr(shape, "Solids", []) if shape is not None else []
        body = solids[0] if len(solids) > 0 else None
        lid = solids[1] if len(solids) > 1 else None

        geometry = EnclosureGeometry(
            body_outer=(
                float(body.BoundBox.XLength) if body else 0.0,
                float(body.BoundBox.YLength) if body else 0.0,
                float(body.BoundBox.ZLength) if body else 0.0,
            ),
            body_inner=(0.0, 0.0, 0.0),
            lid_outer=(
                float(lid.BoundBox.XLength) if lid else 0.0,
                float(lid.BoundBox.YLength) if lid else 0.0,
                float(lid.BoundBox.ZLength) if lid else 0.0,
            ),
            lid_inner=(0.0, 0.0, 0.0),
            body_inner_offset=(0.0, 0.0, 0.0),
            lid_offset=(0.0, 0.0, 0.0),
            lip_outer=(0.0, 0.0, 0.0),
            lip_inner=(0.0, 0.0, 0.0),
            lip_offset=(0.0, 0.0, 0.0),
        )

        now = datetime.now(timezone.utc)
        return EnclosureRecord(
            id=enclosure_id,
            name=feature.Label,
            parameters=parameters,
            body_object_name=f"{feature.Name}_body",
            lid_object_name=f"{feature.Name}_lid",
            geometry=geometry,
            status="valid",
            created_at=now,
            updated_at=now,
            container_object_name=feature.Name,
        )

    def list_enclosures(self) -> list[EnclosureRecord]:
        """List all enclosure records found in the active FreeCAD document."""
        doc = self._doc
        if doc is None:
            return []

        records: list[EnclosureRecord] = []
        for obj in doc.Objects:
            if getattr(obj, "TypeId", "") != "Part::FeaturePython":
                continue
            if hasattr(obj, "EnclosureId") and str(obj.EnclosureId):
                record = self.get_enclosure(str(obj.EnclosureId))
                if record is not None:
                    records.append(record)
        return records

    def apply_data_section_update(
        self,
        enclosure_id: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """Return payload metadata for Data-section recompute integration."""
        return {
            "id": enclosure_id,
            "parameters": parameters,
            "trigger": "data_section_recompute",
        }

    def toggle_visibility(
        self, enclosure_id: str, target: str
    ) -> dict[str, Any] | None:
        """Toggle body/lid visibility flags on a FeaturePython enclosure object."""
        doc = self._doc
        if doc is None:
            return None

        feature = self._find_feature_by_id(enclosure_id)
        if feature is None:
            return None

        target_normalized = target.lower().strip()
        if target_normalized == "body":
            feature.ShowBody = not bool(getattr(feature, "ShowBody", True))
        elif target_normalized == "lid":
            feature.ShowLid = not bool(getattr(feature, "ShowLid", True))
        elif target_normalized in {"both", "all"}:
            next_state = not (
                bool(getattr(feature, "ShowBody", True))
                and bool(getattr(feature, "ShowLid", True))
            )
            feature.ShowBody = next_state
            feature.ShowLid = next_state
        else:
            return None

        doc.recompute()
        return {
            "id": enclosure_id,
            "show_body": bool(getattr(feature, "ShowBody", True)),
            "show_lid": bool(getattr(feature, "ShowLid", True)),
        }

    def _create_feature_object(
        self,
        name: str,
        enclosure_id: str,
        parameters: EnclosureParameters,
    ) -> Any:
        """Create and initialize one `Part::FeaturePython` enclosure object."""
        doc = self._require_doc()

        feature = doc.addObject("Part::FeaturePython", name)
        feature.Label = name
        EnclosureFeatureProxy(feature)
        feature.EnclosureId = enclosure_id
        feature.BodyObjectName = f"{feature.Name}_body"
        feature.LidObjectName = f"{feature.Name}_lid"
        self._set_feature_parameters(feature, parameters)

        if self._app is not None and getattr(self._app, "GuiUp", False):
            try:
                EnclosureViewProvider(feature.ViewObject)
            except Exception:
                pass

        doc.recompute()
        return feature

    def _set_feature_parameters(
        self,
        feature: Any,
        parameters: EnclosureParameters,
    ) -> None:
        """Write domain parameter values into FeaturePython Data properties."""
        feature.Length = float(parameters.length)
        feature.Width = float(parameters.width)
        feature.Height = float(parameters.height)
        feature.WallThickness = float(parameters.wall_thickness)
        feature.LidThickness = float(parameters.lid_thickness)
        feature.Gap = float(parameters.gap)

    def _parameters_from_feature(self, feature: Any) -> EnclosureParameters:
        """Read domain parameters from FeaturePython Data properties."""
        values: dict[str, float] = {}
        for prop_name, param_name in PARAMETER_PROPERTY_MAP.items():
            values[param_name] = float(getattr(feature, prop_name))
        return EnclosureParameters(**values)

    def _find_feature_by_id(self, enclosure_id: str) -> Any | None:
        """Find the FeaturePython object that owns the given enclosure id."""
        doc = self._doc
        if doc is None:
            return None
        for obj in doc.Objects:
            if getattr(obj, "TypeId", "") != "Part::FeaturePython":
                continue
            if hasattr(obj, "EnclosureId") and str(obj.EnclosureId) == enclosure_id:
                return obj
        return None

    def _require_doc(self) -> Any:
        """Return active document or raise when unavailable."""
        if self._doc is None:
            raise RuntimeError("No active FreeCAD document")
        return self._doc
