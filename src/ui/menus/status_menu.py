import pygame

from data.constants import SCREEN_WIDTH
from managers.resource_manager import resource_manager
from utils.load_utils import load_image
from utils.assets_utils import scale_image


class MoneyBar:
    def __init__(self, money):
        self.display_surface = resource_manager.get_display_surf()
        self.base = scale_image(
            load_image("assets/graphics/buttons and surfaces/surface.png"), (150, 60)
        )
        self.font = pygame.font.Font("assets/fonts/LycheeSoda.ttf", 32)
        self.coin_ico = load_image("assets/graphics/icons/coin.png")
        self.money = money
        self.space = 20
        self.padding = 10

    def display(self):
        surf = self.font.render(str(self.money), False, "Black")
        self.display_surface.blit(
            self.base, (SCREEN_WIDTH - self.base.get_width() - 10, self.space)
        )
        self.display_surface.blit(
            self.coin_ico,
            (SCREEN_WIDTH - self.base.get_width() + 10, self.space + self.padding),
        )
        self.display_surface.blit(
            surf,
            (
                SCREEN_WIDTH + self.base.get_width() - self.coin_ico.get_width() - 200,
                self.space + self.padding,
            ),
        )

    def update_value(self, new_value):
        self.money = new_value


class StatusMenu:
    def __init__(self, day):
        self.display_surface = resource_manager.get_display_surf()
        self.base = scale_image(
            load_image("assets/graphics/buttons and surfaces/long surface.png"),
            (700, 60),
        )
        self.font = pygame.font.Font("assets/fonts/CooperBlack.ttf", 28)
        self.space = 20
        self.day = day

    def display(self):
        day_surf = self.font.render(f"Day: {self.day}", False, "Black")
        self.display_surface.blit(self.base, (self.space - 10, self.space))
        self.display_surface.blit(day_surf, (self.space + 10, self.space + 10))

    def update_value(self, new_value):
        self.day = new_value
