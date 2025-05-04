import sys
import os

import pygame


def get_resource_path(relative_path):
    """
    Get the absolute path to a resource, works for development and for PyInstaller.

    Returns the absolute path to a resource.

    - In development mode: Uses the current working directory (assumed to be the project root).
    - In executable mode: Uses sys._MEIPASS, where PyInstaller extracts the bundled files.

    *Note: Made with help of Copilot*
    """
    if hasattr(sys, '_MEIPASS'):  # EXE file, deploying mode
        # noinspection PyProtectedMember
        base_path = sys._MEIPASS
        relative_path = relative_path[3:]  # to drop '../'
    else:  # Development mode
        base_path = os.getcwd()  # Assumes your working directory is set to the project root
    return os.path.normpath(os.path.join(base_path, relative_path))


def import_img(path):
    return pygame.image.load(get_resource_path(path))


def import_audio(path):
    return pygame.mixer.Sound(get_resource_path(path))


def import_folder(path):
    surface_list = []

    path = get_resource_path(path)
    # noinspection PyTypeChecker
    for _, _, img_files in os.walk(path):  # folder_name, sub_folder, img_files
        for image in img_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)

    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    path = get_resource_path(path)
    # noinspection PyTypeChecker
    for _, _, img_files in os.walk(path):
        for image in img_files:
            full_path = os.path.join(path, image)
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split('.')[0]] = image_surf

    return surface_dict
