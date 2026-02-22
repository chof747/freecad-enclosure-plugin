"""Data model returned by document adapters."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from enclosure_workbench.domain.enclosure_builder import EnclosureGeometry
from enclosure_workbench.domain.parameters import EnclosureParameters


@dataclass
class EnclosureRecord:
    """Transport record representing one persisted enclosure instance."""

    id: str
    name: str
    parameters: EnclosureParameters
    body_object_name: str
    lid_object_name: str
    geometry: EnclosureGeometry
    status: str
    created_at: datetime
    updated_at: datetime
    container_object_name: str | None = None
