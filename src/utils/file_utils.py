import json

def read_json(path: str):
    with open(path, "r") as f:
        data = json.load(f)
    return data

def write_json(file_path: str, data: dict):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

__all__ = ["read_json", "write_json"]
