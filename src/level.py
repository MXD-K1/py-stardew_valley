from random import randint
from typing import Any

import pygame

from data.constants import TILE_SIZE, LAYERS
from managers.resource_manager import resource_manager
from systems.camera import Camera
from ui.overlay import Overlay
from sprites import Particle
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from ui.menus.status_menu import MoneyBar, StatusMenu
from ui.menus.shop_menu import ShopMenu
from ui.menus.settings_menu import SettingMenu
from data_handling import export_data, import_data
from map_loader import MapLoader


class Level:
    def __init__(self) -> None:
        self.display_surface = resource_manager.get_display_surf()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.camera = Camera(self.all_sprites)

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        self.map_loader = MapLoader(
            self.all_sprites,
            self.collision_sprites,
            self.tree_sprites,
            self.interaction_sprites,
            self.player_add,
            self.soil_layer,
            self.toggle_shop,
        )
        self._setup()

        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        self.day_count = 0

        # Sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # Menus
        self.money_bar = MoneyBar(self.player.money)
        self.setting_menu = SettingMenu()
        self.status_menu = StatusMenu(self.day_count)

        # Shop
        self.menu = ShopMenu(self.player, self.toggle_shop)
        self.shop_active = False

        # Sound (music)
        self.play_sound = True
        resource_manager.play_sound("bg_music", -1)

        # self.inventory = Inventory(self.player)

        # Getting data
        self.load_game_data()

    def _setup(self) -> None:
        self.player = self.map_loader.load_map("assets/maps/map.tmx")

    def load_game_data(self) -> None:
        data = import_data()
        if data:
            self.player.load_data(data["player"])
            self.raining = data["raining"]
            self.soil_layer.raining = self.raining
            self.soil_layer.load_data(data["farming data"])
            self.load_data(data)

    def load_data(self, data: dict) -> None:
        self.day_count = data["day_count"]
        self.play_sound = data["settings"]["sound"]
        self.setting_menu.sound_switch.play_sound = self.play_sound
        if self.play_sound:
            resource_manager.play_sound("bg_music", -1)

    def save_data(self) -> dict[str, Any]:
        return {
            "player": self.player.save_data(),
            "raining": self.raining,
            "day_count": self.day_count,
            "farming data": self.soil_layer.save_data(),
        }

    def save_game_data(self) -> None:
        export_data(self)

    def player_add(self, item, amount: int = 1) -> None:
        self.player.item_inventory[item] += amount
        resource_manager.play_sound("success")

    def toggle_shop(self) -> None:
        self.shop_active = not self.shop_active

    def reset(self) -> None:
        # New day

        # Plants
        self.soil_layer.update_plants()

        # Soil
        self.soil_layer.remove_water()

        # Randomize the rain
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.remove_water()
            self.soil_layer.water_all()

        # Trees and apples
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

        # Sky
        self.sky.start_color = [255, 255, 255]

        # Days
        self.day_count += 1

        # Saving data
        export_data(self)  # When sleeping

    def plant_collision(self) -> None:
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    # noinspection PyTypeChecker
                    Particle(
                        plant.rect.topleft,
                        plant.image,
                        self.all_sprites,
                        z=LAYERS["main"],
                    )

                    (
                        self.soil_layer.grid[plant.rect.centery // TILE_SIZE][
                            plant.rect.centerx // TILE_SIZE
                        ]["Planting info"]["Planted"]
                    ) = False
                    (
                        self.soil_layer.grid[plant.rect.centery // TILE_SIZE][
                            plant.rect.centerx // TILE_SIZE
                        ]["Planting info"]["Seed"]
                    ) = None
                    (
                        self.soil_layer.grid[plant.rect.centery // TILE_SIZE][
                            plant.rect.centerx // TILE_SIZE
                        ]["Planting info"]["Age"]
                    ) = 0

    def get_current_settings(self) -> None:
        self.play_sound = self.setting_menu.sound_switch.play_sound
        self.settings = {"play sound": self.play_sound}

    def run(self, dt: float) -> None:
        # Drawing logic
        self.camera.custom_draw(self.player)

        # Updates
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)  # Call update in sprites
            self.plant_collision()

        # Weather
        self.overlay.display()
        # Weather -> Raining
        if self.raining and not self.shop_active and not self.setting_menu.toggled:
            self.rain.update()

        # Daytime
        self.sky.display(dt)

        # Transition overlay
        if self.player.sleep:
            self.transition.play()

        if not self.shop_active:
            # Money
            self.money_bar.update_value(self.player.money)
            self.money_bar.display()

            # Settings
            self.get_current_settings()
            self.setting_menu.display(self.settings)

            # Sound playing in settings
            if not self.play_sound:
                # pygame.mixer.pause()
                resource_manager.stop_sound("bg_music")
            else:
                pass
                # pygame.mixer.unpause()
                # self.music.play(loops=-1)

            # Status Menu
            self.status_menu.update_value(self.day_count)
            self.status_menu.display()

            # Inventory
            # self.inventory.display()
            # self.inventory.update()
