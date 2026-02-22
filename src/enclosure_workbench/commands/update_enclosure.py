"""Update enclosure command implementation."""

from __future__ import annotations

from enclosure_workbench.domain.enclosure_builder import EnclosureBuilder
from enclosure_workbench.domain.parameters import (
    ParameterValidationError,
    merge_parameters,
    validate_parameters,
)
from enclosure_workbench.domain.results import CommandResult, failure, success
from enclosure_workbench.integration.document_adapter import DocumentAdapter
from enclosure_workbench.integration.freecad_document import FreeCADDocumentAdapter


def update_enclosure_set(
    enclosure_id: str,
    parameters: dict[str, float],
    *,
    document: DocumentAdapter | None = None,
    builder: EnclosureBuilder | None = None,
) -> CommandResult:
    """Update an existing enclosure set by id and recompute its geometry."""
    adapter: DocumentAdapter = document or FreeCADDocumentAdapter()
    enclosure_builder = builder or EnclosureBuilder()

    record = adapter.get_enclosure(enclosure_id)
    if record is None:
        return failure("not_found", f"Enclosure id '{enclosure_id}' was not found")

    merged = merge_parameters(parameters, base=record.parameters)
    try:
        validate_parameters(merged)
    except ParameterValidationError as exc:
        return failure("validation_error", str(exc))

    geometry = enclosure_builder.build(merged)
    updated = adapter.update_enclosure(enclosure_id, merged, geometry)

    return success(
        {
            "id": updated.id,
            "name": updated.name,
            "parameters": updated.parameters.to_dict(),
            "body_object_name": updated.body_object_name,
            "lid_object_name": updated.lid_object_name,
            "status": updated.status,
        }
    )
