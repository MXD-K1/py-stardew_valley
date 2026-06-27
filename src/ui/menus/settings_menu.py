import pygame

from data.constants import SCREEN_WIDTH
from managers.resource_manager import resource_manager
from timer import Timer
from utils.load_utils import load_image
from utils.assets_utils import scale_image


class Switch:
    def __init__(self):
        self.switch_on_ico = scale_image(
            load_image("assets/graphics/buttons and surfaces/switch on.png"), (50, 30)
        )
        self.switch_off_ico = scale_image(
            load_image("assets/graphics/buttons and surfaces/switch off.png"), (50, 30)
        )

        self.timer = Timer(200, self.toggle)
        self.play_sound = False

    def get_surf(self, play_sound):
        self.play_sound = play_sound
        self.surf = self.switch_on_ico if play_sound else self.switch_off_ico

    def toggle(self):
        self.play_sound = not self.play_sound

    def check_pressed(self, rect):
        mouse_pos = pygame.mouse.get_pos()
        left_button_pressed = pygame.mouse.get_pressed()[0]
        if rect.collidepoint(mouse_pos) and left_button_pressed:
            self.timer.activate()


class SettingMenu:
    def __init__(self):
        self.display_surface = resource_manager.get_display_surf()
        self.base = scale_image(
            load_image("assets/graphics/buttons and surfaces/sq_button.png"), (50, 50)
        )
        self.font = pygame.font.Font("assets/fonts/LycheeSoda.ttf", 32)
        self.setting_ico = scale_image(
            load_image("assets/graphics/icons/settings.png"), (25, 25)
        )
        self.setting_pad = scale_image(
            load_image("assets/graphics/buttons and surfaces/setting pad.png"),
            (300, 400),
        )
        self.space = 25

        self.pos = (SCREEN_WIDTH - self.setting_pad.get_width() - 100, 90)

        self.toggled = False
        self.timer = Timer(200, self.toggle)

        self.items = []

        self.sound_ico = load_image("assets/graphics/icons/sound.png")
        self.sound_switch = Switch()
        self.add_item(self.sound_switch)

    def display(self, settings):
        base_rect = self.base.get_rect()
        base_rect.topleft = (SCREEN_WIDTH - self.base.get_width() - 15, self.space + 60)
        ico_rect = self.setting_ico.get_rect()
        ico_rect.centerx, ico_rect.centery = base_rect.centerx, base_rect.centery - 2
        self.display_surface.blit(self.base, base_rect)
        self.display_surface.blit(self.setting_ico, ico_rect)

        if self.timer.active:
            self.timer.update()
        self.check_pressed(base_rect)

        if self.toggled:
            self.display_setting_menu(settings)

            if self.sound_switch.timer.active:
                self.sound_switch.timer.update()

    def check_pressed(self, rect):
        mouse_pos = pygame.mouse.get_pos()
        left_button_pressed = pygame.mouse.get_pressed()[0]
        if rect.collidepoint(mouse_pos) and left_button_pressed:
            self.timer.activate()

    def toggle(self):
        self.toggled = not self.toggled

    def display_setting_menu(self, settings):
        self.display_surface.blit(self.setting_pad, self.pos)
        self.display_surface.blit(self.sound_ico, (self.pos[0] + 20, self.pos[1] + 110))

        for index, item in enumerate(self.items):
            item.get_surf(settings["play sound"])
            rect = pygame.Rect(
                self.pos[0] + self.setting_pad.get_width() - 60,
                self.pos[1] + 120 + (self.space * index),
                50,
                30,
            )
            item.check_pressed(rect)
            self.display_surface.blit(
                item.surf,
                (
                    self.pos[0] + self.setting_pad.get_width() - 60,
                    self.pos[1] + 120 + (self.space * index),
                ),
            )

    def add_item(self, item):
        """Add a setting to settings."""
        self.items.append(item)
