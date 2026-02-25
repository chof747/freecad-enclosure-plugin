from time import perf_counter

from enclosure_workbench.commands.create_enclosure import create_enclosure_set
from enclosure_workbench.commands.update_enclosure import update_enclosure_set


def test_performance_thresholds(writable_document, object_registry) -> None:
    start_create = perf_counter()
    created = create_enclosure_set(document=writable_document, registry=object_registry)
    create_elapsed = perf_counter() - start_create
    assert created.ok is True
    assert create_elapsed < 2.0

    start_update = perf_counter()
    updated = update_enclosure_set(
        created.payload["id"], {"gap": 0.22}, document=writable_document
    )
    update_elapsed = perf_counter() - start_update
    assert updated.ok is True
    assert update_elapsed < 1.0
