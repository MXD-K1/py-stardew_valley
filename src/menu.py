import time

import pygame

from settings import *
from support import get_resource_path, import_img
from timer import Timer


class Menu:
    def __init__(self, player, toggle_menu):
        # General setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(get_resource_path("assets/fonts/LycheeSoda.ttf"), 30)

        # Options
        self.width = 400
        self.space = 10
        self.padding = 8

        # Entries
        self.options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys())
        self.sell_border = len(self.player.item_inventory) - 1
        self.setup()

        # Movement
        self.index = 0  # default
        self.timer = Timer(200)

    def display_money(self):
        money_surf = self.font.render(f' {self.player.money} ', False, 'Black')
        money_rect = money_surf.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))

        pygame.draw.rect(self.display_surface, 'White', money_rect.copy().inflate(10, 10),
                         0, 6)
        self.display_surface.blit(money_surf, money_rect)

    def setup(self):
        # Create text surfaces
        self.text_surfs = []
        self.total_height = 0
        for item in self.options:
            text_surf = self.font.render(item, False, 'Black')
            self.text_surfs.append(text_surf)
            self.total_height += text_surf.get_height() + self.padding * 2

        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(SCREEN_WIDTH / 2 - self.width / 2, self.menu_top, self.width, self.total_height)

        # Buy / sell text surface
        self.buy_text = self.font.render('buy', False, 'Black')
        self.sell_text = self.font.render('sell', False, 'Black')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

        if not self.timer.active:
            if keys[pygame.K_UP]:
                self.index -= 1
                self.timer.activate()
            if keys[pygame.K_DOWN]:
                self.index += 1
                self.timer.activate()

            if keys[pygame.K_SPACE]:
                self.timer.activate()

                # Get item
                current_item = self.options[self.index]

                # Sell
                if self.index <= self.sell_border:
                    if self.player.item_inventory[current_item] > 0:
                        self.player.item_inventory[current_item] -= 1
                        self.player.money += SALE_PRICES[current_item]

                # Buy
                else:
                    seed_price = PURCHASE_PRICES[current_item]
                    if self.player.money >= seed_price:
                        self.player.seed_inventory[current_item] += 1
                        self.player.money -= seed_price

        # Clam the values
        if self.index < 0:
            self.index = len(self.options) - 1
        if self.index > len(self.options) - 1:
            self.index = 0

    def show_entry(self, text_surf, amount, top, selected):
        # Background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + self.padding * 2)
        pygame.draw.rect(self.display_surface, 'White', bg_rect, 0, 4)

        # Text
        text_rect = text_surf.get_rect(midleft=(self.main_rect.left + 20, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        # Amount
        amount_surf = self.font.render(str(amount), False, 'Black')
        amount_rect = amount_surf.get_rect(midright=(self.main_rect.right - 20, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        # Selected
        if selected:
            pygame.draw.rect(self.display_surface, 'Black', bg_rect, 4, 4)
            if self.index <= self.sell_border:  # Sell
                pos_rect = self.sell_text.get_rect(midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.sell_text, pos_rect)
            else:  # Buy
                pos_rect = self.buy_text.get_rect(midleft=(self.main_rect.left + 150, bg_rect.centery))
                self.display_surface.blit(self.buy_text, pos_rect)

    def update(self):
        self.input()
        self.display_money()
        # The hidden rect, for testing
        # pygame.draw.rect(self.display_surface, 'red', self.main_rect)

        for text_index, text_surf in enumerate(self.text_surfs):
            top = self.main_rect.top + text_index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[text_index]
            self.show_entry(text_surf, amount, top, self.index == text_index)


class MoneyBar:
    def __init__(self, money):
        self.display_surface = pygame.display.get_surface()
        self.base = pygame.transform.scale(import_img("assets/graphics/buttons and surfaces/surface.png"),
                                           (150, 60))
        self.font = pygame.font.Font(get_resource_path("assets/fonts/LycheeSoda.ttf"), 32)
        self.coin_ico = import_img("assets/graphics/icons/coin.png")
        self.money = money
        self.space = 20
        self.padding = 10

    def display(self):
        surf = self.font.render(str(self.money), False, "Black")
        self.display_surface.blit(self.base, (SCREEN_WIDTH - self.base.get_width() - 10, self.space))
        self.display_surface.blit(self.coin_ico, (SCREEN_WIDTH - self.base.get_width() + 10, self.space +
                                                  self.padding))
        self.display_surface.blit(surf, (SCREEN_WIDTH + self.base.get_width() - self.coin_ico.get_width() - 200,
                                         self.space + self.padding))

    def update_value(self, new_value):
        self.money = new_value


class SettingMenu:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.base = pygame.transform.scale(import_img("assets/graphics/buttons and surfaces/sq_button.png"), (50, 50))
        self.font = pygame.font.Font(get_resource_path("assets/fonts/LycheeSoda.ttf"), 32)
        self.setting_ico = pygame.transform.scale(import_img("assets/graphics/icons/settings.png"), (25, 25))
        self.setting_pad = pygame.transform.scale(import_img("assets/graphics/buttons and surfaces/setting pad.png"),
                                                  (300, 400))
        self.space = 25

        self.pos = (SCREEN_WIDTH - self.setting_pad.get_width() - 100, 90)

        self.toggled = False
        self.timer = Timer(200, self.toggle)

        self.items = []

        self.sound_ico = import_img("assets/graphics/icons/sound.png")
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
            item.get_surf(settings['play sound'])
            rect = pygame.Rect(self.pos[0] + self.setting_pad.get_width() - 60,
                               self.pos[1] + 120 + (self.space * index), 50, 30)
            item.check_pressed(rect)
            self.display_surface.blit(item.surf, (self.pos[0] + self.setting_pad.get_width() - 60,
                                                  self.pos[1] + 120 + (self.space * index)))

    def add_item(self, item):
        """Add a setting to settings."""
        self.items.append(item)


class StatusMenu:
    def __init__(self, day):
        self.display_surface = pygame.display.get_surface()
        self.base = pygame.transform.scale(import_img("assets/graphics/buttons and surfaces/long surface.png"),
                                           (700, 60))
        self.font = pygame.font.Font(get_resource_path("assets/fonts/CooperBlack.ttf"), 28)
        self.space = 20
        self.day = day

    def display(self):
        day_surf = self.font.render(f"Day: {self.day}", False, "Black")
        self.display_surface.blit(self.base, (self.space - 10, self.space))
        self.display_surface.blit(day_surf, (self.space + 10, self.space + 10))

    def update_value(self, new_value):
        self.day = new_value


class Switch:
    def __init__(self):
        self.switch_on_ico = pygame.transform.scale(import_img("assets/graphics/buttons and surfaces/switch on.png"),
                                                    (50, 30))
        self.switch_off_ico = pygame.transform.scale(import_img(
            "assets/graphics/buttons and surfaces/switch off.png"),
                                                     (50, 30))

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


class Inventory:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.base = pygame.transform.scale(import_img("assets/graphics/buttons and surfaces/inventory.png"),
                                           (450, 90))
        self.font = pygame.font.Font(get_resource_path("assets/fonts/LycheeSoda.ttf"), 26)

        self.selected = 1  # for counting purpose only
        self.highlight_box_place = [SCREEN_WIDTH // 2 - self.base.get_width() // 2 + 11, SCREEN_HEIGHT - 90]
        self.timer = Timer(250)

        self.items = ['axe', 'hoe', 'water']
        self.inventory_items = [['axe', 1], ['hoe', 1], ['water', 1]]
        self.player = player

        self.item_surfs = self.load_assets()

        self.count_limit = 99

    @staticmethod
    def load_assets():
        names = ["axe", "hoe", "water", "apple", "wood"]
        surfs = {name: pygame.transform.scale(import_img(f"assets/graphics/inventory items/{name}.png"),
                                              (32, 38)) for name in names}
        return surfs

    def display(self):
        self.base_rect = self.base.get_rect()
        self.base_rect.center = SCREEN_WIDTH // 2 - self.base.get_width() // 2, SCREEN_HEIGHT - 100
        self.display_surface.blit(self.base, self.base_rect.center)

    def display_item(self, item, index, amount=None):
        img = self.item_surfs[item]
        rect = (SCREEN_WIDTH // 2 - self.base.get_width() // 2 + INVENTORY_ITEM_PLACES[index][0],
                SCREEN_HEIGHT - 100 + INVENTORY_ITEM_PLACES[index][1])
        self.display_surface.blit(img, rect)

        countable = {'apple', 'wood'}
        if item in countable:
            if amount is None:
                raise ValueError("No amount provided with a countable item.")
            font = self.font.render(f'{amount}', False, 'black')
            if amount > 19:
                x = 20
            elif amount > 9:
                x = 24
            else:
                x = 30
            self.display_surface.blit(font, (rect[0] + x, rect[1] + 18))

    def check_existence_and_display(self, item):  # Needs refactoring
        inventory = {**self.player.item_inventory, **self.player.tool_inventory}
        items = (_item[0] for _item in self.inventory_items)
        if inventory[item] > 0 and item not in items:
            if inventory[item] > 99:
                groups = (inventory[item] // 99 if inventory[item] % 99 == 0
                          else inventory[item] // 99 + 1)
                for group in range(groups):
                    self.inventory_items.append([item, 99 if not group + 1 == groups else
                                                inventory[item] % 99])
            else:
                self.inventory_items.append([item, inventory[item]])

        elif inventory[item] == 0 and item in items:
            if inventory[item] > 99:
                groups = (inventory[item] // 99 if inventory[item] % 99 == 0
                          else inventory[item] // 99 + 1)
                for group in range(groups):
                    self.inventory_items.remove([item, 99 if not group + 1 == groups else
                                                inventory[item] % 99])
            else:
                self.inventory_items.remove([item, inventory[item]])

        self.display_items(inventory)

    def display_items(self, inventory):
        for index, (_item, amount) in enumerate(inventory.items()):
            try:
                self.display_item(_item, index + 1, amount)  # + 1 for counting purpose only
            except KeyError:
                pass

    def highlight(self, left, top):
        rect = pygame.Rect(left, top, 55, 54)
        pygame.draw.rect(self.display_surface, 'white', rect, 3, 8)

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if not self.timer.active:
            if keys[pygame.K_d]:
                if self.selected >= 7:
                    self.selected = 1
                    self.highlight_box_place[0] = SCREEN_WIDTH // 2 - self.base.get_width() // 2 + 11
                else:
                    if self.selected == 3 or self.selected == 4:  # ==3 ? to start working from 4, why I have no idea
                        self.highlight_box_place[0] += 1  # to look nice, the problem is that the distances
                        # aren't completely equal
                    self.highlight_box_place[0] += 62
                    self.selected += 1

                self.timer.activate()

            if keys[pygame.K_a]:
                if self.selected <= 1:
                    self.selected = 7
                    self.highlight_box_place[0] += (62 * (self.selected - 1) + 2)
                else:
                    if self.selected == 5 or self.selected == 4:  # ==3 ? to start working from 4, why I have no idea
                        self.highlight_box_place[0] -= 1
                    self.highlight_box_place[0] -= 62
                    self.selected -= 1

                self.timer.activate()

            if keys[pygame.K_RETURN]:
                if self.selected in (1, 2, 3):
                    self.player.selected_tool = self.items[self.selected - 1]

            self.highlight(*self.highlight_box_place)

    def update_items(self):
        # inventory = {value for value in self.player.item_inventory.items()} a little faster but still slow
        for item, count in self.player.item_inventory.items():
            if count > 0:
                self.items.append(item)

    def update(self):
        self.display()
        self.input()

        self.update_items()  # the game slows down here

        for item in self.items:
            self.check_existence_and_display(item)
