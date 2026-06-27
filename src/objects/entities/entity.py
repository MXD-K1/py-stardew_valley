from collections.abc import Iterable

import pygame

from data.constants import LAYERS
from utils.math_utils import sin, Vector2


class Entity(pygame.sprite.Sprite):
    def __init__(
        self,
        image: pygame.Surface,
        pos: Vector2 | tuple[float, float],
        speed: int = 0,
        groups: Iterable[pygame.sprite.Group] | None = None,
    ) -> None:
        super().__init__(*(groups if groups else []))
        self.z = LAYERS["main"]

        self.image = image
        self.rect = self.image.get_frect(center=pos)

        self.direction = Vector2()
        self.pos = Vector2(self.rect.center)
        self.speed = speed

    def move(self, dt: float) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal Movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = self.pos.x

        # Vertical Movement
        self.pos.y += self.direction.y * self.speed * dt
        self.rect.centery = self.pos.y

    @staticmethod
    def get_wave_value() -> int:  # used to get alpha
        value = sin(pygame.time.get_ticks())
        return 255 if value >= 0 else 0
