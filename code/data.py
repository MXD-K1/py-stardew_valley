import json

from support import get_resource_path


def export_data(player, raining, day_count, grid_data):
    data = {
        'player': {
            'pos': list(player.pos),
            'inventories': {
                    'item inventory': player.item_inventory,
                    'seed inventory': player.seed_inventory},
            'money': player.money,
            'selected tool': player.selected_tool,
            'selected seed': player.selected_seed
        },
        'raining': raining,
        'day count': day_count,
        'farming data': grid_data,
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
