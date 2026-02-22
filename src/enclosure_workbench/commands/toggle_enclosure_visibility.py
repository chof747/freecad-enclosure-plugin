"""Toggle visibility flags for enclosure body/lid in FeaturePython object."""

from __future__ import annotations

from enclosure_workbench.domain.results import CommandResult, failure, success
from enclosure_workbench.integration.document_adapter import DocumentAdapter
from enclosure_workbench.integration.freecad_document import FreeCADDocumentAdapter


def toggle_enclosure_visibility(
    enclosure_id: str,
    target: str,
    *,
    document: DocumentAdapter | None = None,
) -> CommandResult:
    adapter: DocumentAdapter = document or FreeCADDocumentAdapter()
    record = adapter.get_enclosure(enclosure_id)
    if record is None:
        return failure("not_found", f"Enclosure id '{enclosure_id}' was not found")

    toggled = adapter.toggle_visibility(enclosure_id, target)
    if toggled is None:
        return failure("not_found", f"Enclosure id '{enclosure_id}' was not found")
    return success(toggled)
