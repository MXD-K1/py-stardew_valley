from collections.abc import Iterable

import pygame

from config import LAYERS
from utils.math_utils import sin


class Entity(pygame.sprite.Sprite):
    def __init__(self, groups: Iterable[pygame.sprite.Group]):
        super().__init__(*groups)
        self.z = LAYERS['main']

    @staticmethod
    def get_wave_value():  # used to get alpha
        value = sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0
