import os

from pygame import Surface
from pygame.image import load
from pygame.mixer import Sound
from pygame.transform import scale
from pytmx import TiledMap
from pytmx.util_pygame import load_pygame


def load_image(path: str) -> Surface:
    return load(path).convert_alpha()


def load_sound(path: str) -> Sound:
    return Sound(path)


def load_map(path: str) -> TiledMap:
    return load_pygame(path)


def load_folder_of_images(path: str) -> list:
    images_list = []

    _, _, images = next(os.walk(path))  # folder_name, sub_folder, files
    for image_path in images:
        full_path = os.path.join(path, image_path)
        image_surf = load_image(full_path)
        images_list.append(image_surf)

    return images_list


def load_folder_of_images_as_dict(path: str) -> dict:
    images_dict = {}

    _, _, images = next(os.walk(path))
    for image_path in images:
        full_path = os.path.join(path, image_path)
        image_surf = load_image(full_path)
        images_dict[image_path.rsplit(".")[0]] = image_surf

    return images_dict


def cut_spritesheet(spritesheet_path: str, cols: int, rows: int) -> dict[tuple[int, int], Surface]:
    spritesheet = load_image(spritesheet_path)
    frames = {}

    cell_width = spritesheet.get_width() / cols
    cell_height = spritesheet.get_height() / rows

    for col in range(cols):
        for row in range(rows):
            surf = spritesheet.subsurface(
                (col * cell_width, row * cell_height, cell_width, cell_height)
            ).copy()
            surf = scale(surf, (surf.get_width(), surf.get_height())).copy()
            frames[(row, col)] = surf
    return frames


__all__ = [
    "load_image",
    "load_sound",
    "load_map",
    "load_folder_of_images",
    "load_folder_of_images_as_dict",
    "cut_spritesheet",
]
