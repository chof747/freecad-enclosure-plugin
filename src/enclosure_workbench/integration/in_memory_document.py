"""In-memory document adapter for tests and headless scenarios."""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime, timezone
from typing import Any

from enclosure_workbench.domain.enclosure_builder import EnclosureGeometry
from enclosure_workbench.domain.parameters import EnclosureParameters
from enclosure_workbench.integration.enclosure_record import EnclosureRecord


class InMemoryDocumentAdapter:
    """Lightweight adapter used by tests when FreeCAD is not involved."""

    def __init__(self, writable: bool = True) -> None:
        """Initialize an in-memory store and visibility state map."""
        self._writable = writable
        self._records: dict[str, EnclosureRecord] = {}
        self._visibility: dict[str, dict[str, bool]] = {}

    def is_writable(self) -> bool:
        """Return the configured write capability for this adapter."""
        return self._writable

    def add_enclosure(
        self,
        enclosure_id: str,
        name: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord:
        """Store a newly created enclosure record in memory."""
        now = datetime.now(timezone.utc)
        record = EnclosureRecord(
            id=enclosure_id,
            name=name,
            parameters=parameters,
            body_object_name=f"{name}_body",
            lid_object_name=f"{name}_lid",
            geometry=geometry,
            status="valid",
            created_at=now,
            updated_at=now,
            container_object_name=name,
        )
        self._records[enclosure_id] = record
        self._visibility[enclosure_id] = {"body": True, "lid": True}
        return deepcopy(record)

    def update_enclosure(
        self,
        enclosure_id: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord:
        """Update an existing in-memory enclosure entry."""
        record = self._records[enclosure_id]
        record.parameters = parameters
        record.geometry = geometry
        record.updated_at = datetime.now(timezone.utc)
        return deepcopy(record)

    def get_enclosure(self, enclosure_id: str) -> EnclosureRecord | None:
        """Return a copy of one enclosure record by id, if present."""
        record = self._records.get(enclosure_id)
        return deepcopy(record) if record else None

    def list_enclosures(self) -> list[EnclosureRecord]:
        """Return copies of all enclosure records."""
        return [deepcopy(record) for record in self._records.values()]

    def apply_data_section_update(
        self,
        enclosure_id: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """Return metadata payload for Data-section update tests."""
        return {
            "id": enclosure_id,
            "parameters": parameters,
            "trigger": "data_section_recompute",
        }

    def toggle_visibility(
        self, enclosure_id: str, target: str
    ) -> dict[str, Any] | None:
        """Toggle stored visibility flags for body/lid entries."""
        if enclosure_id not in self._records:
            return None

        vis = self._visibility.setdefault(enclosure_id, {"body": True, "lid": True})
        key = target.lower().strip()
        if key == "body":
            vis["body"] = not vis["body"]
        elif key == "lid":
            vis["lid"] = not vis["lid"]
        elif key in {"both", "all"}:
            next_state = not (vis["body"] and vis["lid"])
            vis["body"] = next_state
            vis["lid"] = next_state
        else:
            return None

        return {
            "id": enclosure_id,
            "show_body": vis["body"],
            "show_lid": vis["lid"],
        }
