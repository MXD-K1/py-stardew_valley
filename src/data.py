import json

from utils.file_utils import write_json, read_json


def export_data(level) -> None:
    data = {
        'player': {
            'pos': list(level.player.pos),
            'inventories': {
                    'item inventory': level.player.item_inventory,
                    'seed inventory': level.player.seed_inventory},
            'money': level.player.money,
            'selected tool': level.player.selected_tool,
            'selected seed': level.player.selected_seed
        },
        'time': None,  # Empty for now
        'raining': level.raining,
        'day count': level.day_count,
        'settings': {
            'sound': level.play_sound,
        },
        'Trees data': None,  # Empty for now
        'farming data': level.soil_layer.grid,
    }  # groups can't be stored there

    write_json("playing data/data.json", data)


def import_data() -> dict:
    try:
        return read_json("playing data/data.json")
    except (FileNotFoundError, json.JSONDecodeError):
        write_json("playing data/data.json", {})
        return {}
