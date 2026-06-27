import json


def read_json(path: str) -> dict:
    with open(path, "r") as f:
        data = json.load(f)
    return data


def write_json(file_path: str, data: dict) -> None:
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


__all__ = ["read_json", "write_json"]
