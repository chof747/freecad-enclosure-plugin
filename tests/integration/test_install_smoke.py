from pathlib import Path


def test_install_smoke_scripts_exist() -> None:
    root = Path(__file__).resolve().parents[2]
    assert (root / "scripts" / "install-local.sh").exists()
    assert (root / "scripts" / "update-local.sh").exists()
    assert (root / "scripts" / "smoke-freecad.sh").exists()
