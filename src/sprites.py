from random import randint, choice
from typing import Iterable

import pygame

from utils.load_utils import load_image
from utils.math_utils import Vector2
from data.constants import APPLE_POS, LAYERS


class Generic(pygame.sprite.Sprite):
    def __init__(self, pos: Vector2 | tuple[float, float], surf: pygame.Surface, groups: Iterable[pygame.sprite.Group], z=LAYERS["main"]) -> None:
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(
            -self.rect.width * 0.2, -self.rect.height * 0.3
        )
        # width must be small


class Interaction(Generic):
    def __init__(self, pos:  Vector2 | tuple[float, float], size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)

        self.name = name


class Water(Generic):
    def __init__(self, pos: Vector2 | tuple[float, float], frames, groups):
        # Animation setup
        self.frames = frames
        self.frame_index = 0
        # no need for hitbox

        # Sprite setup
        super().__init__(
            pos, surf=self.frames[self.frame_index], groups=groups, z=LAYERS["water"]
        )

    def animate(self, dt: float) -> None:
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt: float) -> None:
        self.animate(dt)


class WildFlower(Generic):
    def __init__(self, pos: Vector2 | tuple[float, float], surf: pygame.Surface, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)


class Particle(Generic):
    def __init__(self, pos: Vector2 | tuple[float, float], surf: pygame.Surface, groups, z, duration=200):
        super().__init__(pos, surf, groups, z)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()  # watch and see!
        new_surf.set_colorkey((0, 0, 0))
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()


class Tree(Generic):
    def __init__(self, pos: Vector2 | tuple[float, float], surf, groups, name, player_add) -> None:
        super().__init__(pos, surf, groups)
        # hit box the same as in generic
        self.name = name

        # Tree attributes
        self.health = 5
        self.alive = True
        stump_path = f"assets/graphics/stumps/{name.lower()}.png"
        self.stump_surf = load_image(stump_path).convert_alpha()  # when dead

        # Apples
        self.apple_surf = load_image("assets/graphics/fruit/apple.png")
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites: pygame.sprite.Group = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add

    def damage(self) -> None:
        # Damage tree
        self.health -= 1

        # Remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            # print(self.groups())
            # noinspection PyTypeChecker
            Particle(
                random_apple.rect.topleft,
                random_apple.image,
                sorted(self.groups(), key=lambda group: len(group.sprites()))[2],
                LAYERS["fruit"],
            )
            self.player_add("apple")
            random_apple.kill()

    def check_death(self) -> None:
        if self.health <= 0:
            # noinspection PyTypeChecker
            Particle(
                self.rect.topleft,
                self.image,
                sorted(self.groups(), key=lambda group: len(group.sprites()))[2],
                LAYERS["fruit"],
                300,
            )
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            self.player_add("wood", randint(1, 3) if self.name == "Large" else 1)

    def update(self, dt: float) -> None:
        if self.alive:
            self.check_death()

    def create_fruit(self) -> None:
        for pos in self.apple_pos:
            if randint(0, 10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                # print(self.groups())

                # noinspection PyTypeChecker
                Generic(
                    (x, y),
                    self.apple_surf,
                    [
                        self.apple_sprites,
                        sorted(
                            self.groups(),
                            key=lambda group: len(group.sprites()),
                            reverse=True,
                        )[0],
                    ],
                    # sorted to solve unknown problem
                    z=LAYERS["fruit"],
                )
