from enclosure_workbench.commands.create_enclosure import create_enclosure_set


def test_create_enclosure_set_returns_contract_payload(
    writable_document, object_registry
) -> None:
    result = create_enclosure_set(document=writable_document, registry=object_registry)

    assert result.ok is True
    payload = result.payload
    assert payload is not None
    assert payload["id"].startswith("enclosure_")
    assert payload["name"]
    assert payload["status"] == "valid"
    assert payload["body_object_name"].endswith("_body")
    assert payload["lid_object_name"].endswith("_lid")


def test_create_enclosure_set_validation_error_shape(
    writable_document, object_registry
) -> None:
    result = create_enclosure_set(
        parameters={"wall_thickness": 100.0},
        document=writable_document,
        registry=object_registry,
    )

    assert result.ok is False
    assert result.error is not None
    assert result.error.code == "validation_error"
    assert result.error.message
