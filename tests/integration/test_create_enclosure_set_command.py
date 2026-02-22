from enclosure_workbench.commands.create_enclosure import create_enclosure_set
from enclosure_workbench.commands.update_enclosure import update_enclosure_set
from enclosure_workbench.integration.freecad_document import FreeCADDocumentAdapter


def test_toolbar_create_and_update_flow(writable_document, object_registry) -> None:
    created = create_enclosure_set(document=writable_document, registry=object_registry)
    assert created.ok is True

    payload = created.payload
    assert payload is not None
    enclosure_id = payload["id"]

    updated = update_enclosure_set(
        enclosure_id, {"gap": 0.25}, document=writable_document
    )
    assert updated.ok is True
    assert updated.payload["parameters"]["gap"] == 0.25


def test_no_writable_document_returns_clear_error(
    read_only_document, object_registry
) -> None:
    result = create_enclosure_set(document=read_only_document, registry=object_registry)
    assert result.ok is False
    assert result.error is not None
    assert result.error.code == "document_not_writable"


def test_data_section_update_hook_payload() -> None:
    adapter = FreeCADDocumentAdapter(writable=True)
    payload = adapter.apply_data_section_update("enclosure_001", {"gap": 0.3})
    assert payload["trigger"] == "data_section_recompute"
    assert payload["parameters"]["gap"] == 0.3
