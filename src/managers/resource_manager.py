from typing import Self

import pygame


class ResourceManager:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        self.__display_surf: pygame.Surface | None = None

        self.__surfs: dict[str, pygame.Surface] = {}
        self.__sounds: dict[str, pygame.Sound] = {}

    def set_display_surf(self, display_surf: pygame.Surface) -> None:
        self.__display_surf = display_surf

    def get_display_surf(self) -> pygame.Surface:
        if self.__display_surf is None:
            raise ValueError("Display surface has not been set yet.")
        return self.__display_surf

    def add_sound(self, name: str, sound: pygame.Sound):
        self.__sounds[name] = sound

    def get_sound(self, name: str) -> pygame.Sound:
        return self.__sounds[name]

    def play_sound(self, name: str, loops: int = 0):
        self.__sounds[name].play(loops)

    def stop_sound(self, name: str):
        self.__sounds[name].stop()

    def add_surf(self, name: str, surf: pygame.Surface):
        self.__surfs[name] = surf

    def get_surf(self, name: str) -> pygame.Surface:
        return self.__surfs[name]


resource_manager = ResourceManager()
