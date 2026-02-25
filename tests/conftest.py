"""Shared fixtures for enclosure workbench tests."""

from __future__ import annotations

from pathlib import Path
import sys

import pytest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from enclosure_workbench.integration.in_memory_document import InMemoryDocumentAdapter  # noqa: E402
from enclosure_workbench.integration.object_registry import ObjectRegistry  # noqa: E402


@pytest.fixture
def writable_document() -> InMemoryDocumentAdapter:
    return InMemoryDocumentAdapter(writable=True)


@pytest.fixture
def read_only_document() -> InMemoryDocumentAdapter:
    return InMemoryDocumentAdapter(writable=False)


@pytest.fixture
def object_registry() -> ObjectRegistry:
    return ObjectRegistry()
