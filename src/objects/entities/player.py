from typing import Callable, Any

import pygame

from data.constants import PLAYER_TOOL_OFFSET
from data.controls import KEY_BINDINGS, Action
from objects.entities.entity import Entity
from managers.resource_manager import resource_manager
from soil import SoilLayer
from timer import Timer
from utils.load_utils import load_folder_of_images
from utils.math_utils import Vector2


class Player(Entity):
    def __init__(
        self,
        pos: Vector2 | tuple[float, float],
        group: pygame.sprite.Group,
        collision_sprites: pygame.sprite.Group,
        tree_sprites: pygame.sprite.Group,
        interaction_sprites: pygame.sprite.Group,
        soil_layer: SoilLayer,
        toggle_shop: Callable[[], None],
    ) -> None:
        self.status = "down_idle"  # default
        self.frame_index = 0
        self._import_assets()

        super().__init__(
            self.animations[self.status][self.frame_index], pos, 300, [group]
        )

        # Movement attributes
        self.direction = Vector2()  # or Vector2(0, 0)
        self.pos = Vector2(self.rect.center)
        self.speed = 200

        # Collision
        self.hitbox = self.rect.copy().inflate((-126, -70))  # shrink the rect (w, h)
        self.collision_sprites = collision_sprites

        # Timers
        self.timers = {
            "tool use": Timer(350, self.use_tool),
            "tool switch": Timer(200),
            "seed use": Timer(350, self.use_seed),
            "seed switch": Timer(200),
        }

        # Tools
        self.tools = ["hoe", "axe", "water"]
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

        # Seeds
        self.seeds = ["corn", "tomato"]
        self.seed_index = 0
        self.selected_seed = self.seeds[self.seed_index]

        # Inventory
        self.tool_inventory = {"axe": 1, "hoe": 1, "water": 1}

        self.item_inventory = {"wood": 0, "apple": 0, "corn": 0, "tomato": 0}

        self.seed_inventory = {"corn": 5, "tomato": 0}

        self.money = 200

        # Interaction
        self.tree_sprites = tree_sprites
        self.interaction = interaction_sprites
        self.sleep = False
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

        # Sound
        self.play_sound = True

    def use_tool(self) -> None:
        if self.selected_tool == "hoe":
            self.soil_layer.get_hit(self.target_pos)

        if self.selected_tool == "axe":
            for tree in self.tree_sprites.sprites():
                if tree.rect.collidepoint(self.target_pos):
                    # Play axe sound
                    if self.play_sound:
                        resource_manager.play_sound("axe")
                    tree.damage()

        if self.selected_tool == "water":
            self.soil_layer.water(self.target_pos)

            if self.play_sound:
                resource_manager.play_sound("watering")

    def get_target_pos(self) -> None:
        self.target_pos = (
            self.rect.center + PLAYER_TOOL_OFFSET[self.status.split("_")[0]]
        )

    def use_seed(self) -> None:
        if self.seed_inventory[self.selected_seed] > 0:
            self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
            if self.soil_layer.planted:
                self.seed_inventory[self.selected_seed] -= 1

    def _import_assets(self) -> None:
        self.animations: dict[str, list[pygame.Surface]] = {
            "up": [],
            "down": [],
            "left": [],
            "right": [],
            "right_idle": [],
            "left_idle": [],
            "up_idle": [],
            "down_idle": [],
            "right_hoe": [],
            "left_hoe": [],
            "up_hoe": [],
            "down_hoe": [],
            "right_axe": [],
            "left_axe": [],
            "up_axe": [],
            "down_axe": [],
            "right_water": [],
            "left_water": [],
            "up_water": [],
            "down_water": [],
        }

        for animation in self.animations.keys():
            full_path = "assets/graphics/character/" + animation
            self.animations[animation] = load_folder_of_images(full_path)

    def animate(self, dt: float) -> None:
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0

        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if not self.timers["tool use"].active and not self.sleep:
            if keys[KEY_BINDINGS[Action.MOVE_UP]]:
                self.direction.y = -1
                self.status = "up"
            elif keys[KEY_BINDINGS[Action.MOVE_DOWN]]:
                self.direction.y = 1
                self.status = "down"
            else:
                self.direction.y = 0

            if keys[KEY_BINDINGS[Action.MOVE_RIGHT]]:
                self.direction.x = 1
                self.status = "right"
            elif keys[KEY_BINDINGS[Action.MOVE_LEFT]]:
                self.direction.x = -1
                self.status = "left"
            else:
                self.direction.x = 0

            if keys[KEY_BINDINGS[Action.USE_TOOL]]:
                # Timer for the tool use
                self.timers["tool use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0  # This will reset the animation from 0

            if (
                keys[KEY_BINDINGS[Action.SWITCH_TOOL]]
                and not self.timers["tool switch"].active
            ):
                self.timers["tool switch"].activate()
                self.tool_index += 1
                self.tool_index = (
                    self.tool_index if self.tool_index < len(self.tools) else 0
                )
                self.selected_tool = self.tools[self.tool_index]

            if keys[KEY_BINDINGS[Action.USE_SEED]]:
                self.timers["seed use"].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0  # This will reset the animation from 0

            if (
                keys[KEY_BINDINGS[Action.SWITCH_SEED]]
                and not self.timers["seed switch"].active
            ):
                self.timers["seed switch"].activate()
                self.seed_index += 1
                self.seed_index = (
                    self.seed_index if self.seed_index < len(self.seeds) else 0
                )
                self.selected_seed = self.seeds[self.seed_index]

            if keys[KEY_BINDINGS[Action.INTERACT]]:
                # noinspection PyTypeChecker
                collided_interaction_sprite = pygame.sprite.spritecollide(
                    self, self.interaction, False
                )
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == "Trader":
                        self.toggle_shop()
                    else:  # Bed
                        self.status = "left_idle"
                        self.sleep = True

    def get_status(self):
        # Check if the player is not moving (idling)
        if self.direction.magnitude() == 0:
            self.status = self.status.split("_")[0] + "_idle"

        # Tools
        if self.timers["tool use"].active:
            self.status = self.status = (
                self.status.split("_")[0] + "_" + self.selected_tool
            )

    def update_timers(self) -> None:
        for timer in self.timers.values():
            timer.update()

    def collision(self, direction_str: str) -> None:
        for sprite in self.collision_sprites:
            if hasattr(sprite, "hitbox"):  # to make sure
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction_str == "horizontal":
                        if self.direction.x > 0:  # player moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0:  # player moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction_str == "vertical":
                        if self.direction.y > 0:  # player moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0:  # player moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def move(self, dt: float) -> None:
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()

        # Horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = self.pos.x
        self.rect.centerx = self.hitbox.centerx
        self.collision("horizontal")

        # Vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = self.pos.y
        self.rect.centery = self.hitbox.centery
        self.collision("vertical")

    def update(self, dt: float) -> None:
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()

        self.move(dt)
        self.animate(dt)

    def load_data(self, data: dict) -> None:
        self.money = data["money"]
        self.pos = Vector2(data["pos"])
        self.direction = Vector2(data["dir"])
        self.status = data["dir_str"] + "_idle"
        self.selected_tool = data["selected tool"]
        self.selected_seed = data["selected seed"]
        self.item_inventory = data["inventories"]["item inventory"]
        self.seed_inventory = data["inventories"]["seed inventory"]

    def save_data(self) -> dict[str, Any]:
        return {
            "pos": list(self.pos),
            "dir": list(self.direction),
            "dir_str": self.status.split("_")[0],
            "money": self.money,
            "inventories": {
                "item inventory": self.item_inventory,
                "seed inventory": self.seed_inventory,
            },
            "selected tool": self.selected_tool,
            "selected seed": self.selected_seed,
        }
