import json

from support import get_resource_path


def export_data(level):
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
        'farming data': level.soil_layer.grid,
    }  # groups can't be stored there

    with open(get_resource_path("../playing data/data.json"), 'w') as file:
        json.dump(data, file, indent=4)


def import_data():
    try:
        with open(get_resource_path("../playing data/data.json"), 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        with open(get_resource_path("../playing data/data.json"), 'w') as file:
            json.dump({}, file, indent=4)
