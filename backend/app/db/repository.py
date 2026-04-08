import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


class JsonRepository:
    def __init__(self, file_path: str) -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write({"jobs": [], "candidates": [], "interviews": []})

    def _read(self) -> Dict[str, Any]:
        return json.loads(self.file_path.read_text(encoding="utf-8"))

    def _write(self, payload: Dict[str, Any]) -> None:
        self.file_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")

    def list_items(self, collection: str) -> List[Dict[str, Any]]:
        return self._read().get(collection, [])

    def get_item(self, collection: str, item_id: str) -> Optional[Dict[str, Any]]:
        for item in self.list_items(collection):
            if item.get("id") == item_id:
                return item
        return None

    def upsert_item(self, collection: str, item: Dict[str, Any]) -> Dict[str, Any]:
        data = self._read()
        rows = data.get(collection, [])
        replaced = False
        for idx, row in enumerate(rows):
            if row.get("id") == item.get("id"):
                rows[idx] = item
                replaced = True
                break
        if not replaced:
            rows.append(item)
        data[collection] = rows
        data["updated_at"] = datetime.utcnow().isoformat()
        self._write(data)
        return item
