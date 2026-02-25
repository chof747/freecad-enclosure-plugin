"""Identity and naming helpers for enclosure objects."""

from __future__ import annotations


class ObjectRegistry:
    def __init__(self) -> None:
        self._next_id = 1
        self._id_by_name: dict[str, str] = {}

    def create_identity(self, preferred_name: str | None = None) -> tuple[str, str]:
        enclosure_id = f"enclosure_{self._next_id:03d}"
        base_name = preferred_name if preferred_name else enclosure_id
        name = base_name

        suffix = 1
        while self._name_exists(name):
            suffix += 1
            name = f"{base_name}_{suffix}"

        self._id_by_name[name] = enclosure_id
        self._next_id += 1
        return enclosure_id, name

    def _name_exists(self, name: str) -> bool:
        if name in self._id_by_name:
            return True
        try:
            import FreeCAD as app  # type: ignore

            doc = getattr(app, "ActiveDocument", None)
            if doc is None:
                return False
            return (
                doc.getObject(name) is not None
                or doc.getObject(f"{name}_body") is not None
                or doc.getObject(f"{name}_lid") is not None
            )
        except Exception:
            return False
