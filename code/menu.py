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
        self.font = pygame.font.Font(get_resource_path("../font/LycheeSoda.ttf"), 30)

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
        money_surf = self.font.render(f'${self.player.money}', False, 'Black')
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
        self.base = pygame.transform.scale(import_img("../graphics/money objects/Money surface.png"), (150, 60))
        self.font = pygame.font.Font(get_resource_path("../font/LycheeSoda.ttf"), 32)
        self.coin_ico = import_img("../graphics/money objects/coin.png")
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
