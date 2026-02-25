"""Protocol for enclosure document adapters."""

from __future__ import annotations

from typing import Any, Protocol

from enclosure_workbench.domain.enclosure_builder import EnclosureGeometry
from enclosure_workbench.domain.parameters import EnclosureParameters
from enclosure_workbench.integration.enclosure_record import EnclosureRecord


class DocumentAdapter(Protocol):
    """Abstraction for persistence/retrieval of enclosure objects."""

    def is_writable(self) -> bool:
        """Return True when write operations are currently allowed."""
        ...

    def add_enclosure(
        self,
        enclosure_id: str,
        name: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord:
        """Create and persist a new enclosure record and backing object(s)."""
        ...

    def update_enclosure(
        self,
        enclosure_id: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord:
        """Update an existing enclosure and return the refreshed record."""
        ...

    def get_enclosure(self, enclosure_id: str) -> EnclosureRecord | None:
        """Resolve one enclosure by id, or None when it is missing."""
        ...

    def list_enclosures(self) -> list[EnclosureRecord]:
        """Return all known enclosures in adapter-native order."""
        ...

    def apply_data_section_update(
        self,
        enclosure_id: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """Return integration payload metadata for a Data-section update event."""
        ...

    def toggle_visibility(
        self, enclosure_id: str, target: str
    ) -> dict[str, Any] | None:
        """Toggle body/lid visibility state and return current flags."""
        ...
