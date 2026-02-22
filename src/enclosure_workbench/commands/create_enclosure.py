"""Create enclosure command implementation."""

from __future__ import annotations

from enclosure_workbench.domain.enclosure_builder import EnclosureBuilder
from enclosure_workbench.domain.parameters import (
    ParameterValidationError,
    default_parameters,
    merge_parameters,
    validate_parameters,
)
from enclosure_workbench.domain.results import failure, success, CommandResult
from enclosure_workbench.integration.document_adapter import DocumentAdapter
from enclosure_workbench.integration.freecad_document import FreeCADDocumentAdapter
from enclosure_workbench.integration.object_registry import ObjectRegistry


def create_enclosure_set(
    name: str | None = None,
    parameters: dict[str, float] | None = None,
    *,
    document: DocumentAdapter | None = None,
    registry: ObjectRegistry | None = None,
    builder: EnclosureBuilder | None = None,
) -> CommandResult:
    """Create one enclosure set and persist it through the active adapter.

    The command validates/merges parameters, allocates a unique identity, builds
    deterministic geometry metadata, and returns a stable payload contract.
    """
    adapter: DocumentAdapter = document or FreeCADDocumentAdapter()
    identities = registry or ObjectRegistry()
    enclosure_builder = builder or EnclosureBuilder()

    if not adapter.is_writable():
        return failure(
            "document_not_writable", "No writable FreeCAD document is available"
        )

    merged = merge_parameters(parameters, base=default_parameters())
    try:
        validate_parameters(merged)
    except ParameterValidationError as exc:
        return failure("validation_error", str(exc))

    enclosure_id, enclosure_name = identities.create_identity(name)
    geometry = enclosure_builder.build(merged)
    record = adapter.add_enclosure(enclosure_id, enclosure_name, merged, geometry)

    return success(
        {
            "id": record.id,
            "name": record.name,
            "parameters": record.parameters.to_dict(),
            "body_object_name": record.body_object_name,
            "lid_object_name": record.lid_object_name,
            "status": record.status,
        }
    )
