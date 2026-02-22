from enclosure_workbench.commands.create_enclosure import create_enclosure_set
from enclosure_workbench.commands.update_enclosure import update_enclosure_set


def test_update_enclosure_set_returns_updated_payload(
    writable_document, object_registry
) -> None:
    created = create_enclosure_set(document=writable_document, registry=object_registry)
    enclosure_id = created.payload["id"]

    result = update_enclosure_set(
        enclosure_id, {"gap": 0.15}, document=writable_document
    )

    assert result.ok is True
    payload = result.payload
    assert payload is not None
    assert payload["id"] == enclosure_id
    assert payload["parameters"]["gap"] == 0.15


def test_update_enclosure_set_not_found_error_shape(writable_document) -> None:
    result = update_enclosure_set("missing", {"gap": 0.1}, document=writable_document)

    assert result.ok is False
    assert result.error is not None
    assert result.error.code == "not_found"
    assert "missing" in result.error.message
