import json

from utils.file_utils import write_json, read_json


def export_data(level) -> None:
    data = {
        "time": None,  # Empty for now
        "Trees data": None,  # Empty for now
        "settings": {
            "sound": level.play_sound,
        },
    } | level.save_data()

    write_json("playing data/data.json", data)


def import_data() -> dict:
    try:
        return read_json("playing data/data.json")
    except (FileNotFoundError, json.JSONDecodeError):
        write_json("playing data/data.json", {})
        return {}
