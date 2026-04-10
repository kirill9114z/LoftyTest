import json
import os

STORAGE_FILE = "storage.json"


def _load() -> dict:
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save(data: dict) -> None:
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def set_coordinates(city: str, coordinates: dict) -> None:
    data = _load()
    data[city] = coordinates
    _save(data)


def get_coordinates(city: str) -> dict | None:
    data = _load()
    return data.get(city)



