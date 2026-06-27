import pygame
from typing import Callable

from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from objects.entities.player import Player
from managers.resource_manager import resource_manager


class Transition:
    def __init__(self, reset: Callable, player: Player) -> None:
        # Setup
        self.display_surface = resource_manager.get_display_surf()
        self.reset = reset
        self.player = player

        # Overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255  # white
        self.speed = -2

    def play(self) -> None:
        self.color += self.speed  # will turn to black
        if self.color <= 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed *= -1

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(
            self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
        )
        # pygame.BLEND_RGBA_MULT gets rid of white
