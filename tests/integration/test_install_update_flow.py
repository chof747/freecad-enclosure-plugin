from pathlib import Path


def test_install_update_docs_exist() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "docs" / "installation.md").exists()
    assert (root / "docs" / "deployment.md").exists()
    assert (root / "docs" / "debugging.md").exists()
