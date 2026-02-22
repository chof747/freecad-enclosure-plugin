"""Protocol for enclosure document adapters."""

from __future__ import annotations

from typing import Any, Protocol

from enclosure_workbench.domain.enclosure_builder import EnclosureGeometry
from enclosure_workbench.domain.parameters import EnclosureParameters
from enclosure_workbench.integration.enclosure_record import EnclosureRecord


class DocumentAdapter(Protocol):
    def is_writable(self) -> bool: ...

    def add_enclosure(
        self,
        enclosure_id: str,
        name: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord: ...

    def update_enclosure(
        self,
        enclosure_id: str,
        parameters: EnclosureParameters,
        geometry: EnclosureGeometry,
    ) -> EnclosureRecord: ...

    def get_enclosure(self, enclosure_id: str) -> EnclosureRecord | None: ...

    def list_enclosures(self) -> list[EnclosureRecord]: ...

    def apply_data_section_update(
        self,
        enclosure_id: str,
        parameters: dict[str, Any],
    ) -> dict[str, Any]: ...

    def toggle_visibility(
        self, enclosure_id: str, target: str
    ) -> dict[str, Any] | None: ...
