import pygame

from config import SCREEN_WIDTH, SCREEN_HEIGHT, INVENTORY_ITEM_PLACES
from utils.load_utils import load_image
from utils.assets_utils import scale_image
from managers.resource_manager import resource_manager
from timer import Timer

class Inventory:
    def __init__(self, player):
        self.display_surface = resource_manager.get_display_surf()
        self.base = scale_image(load_image("assets/graphics/buttons and surfaces/inventory.png"),
                                           (450, 90))
        self.font = pygame.font.Font("assets/fonts/LycheeSoda.ttf", 26)

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
        surfs = {
            name: scale_image(load_image(f"assets/graphics/inventory items/{name}.png"), (32, 38)) for name in names
        }
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
                #for group in range(groups):
                #    self.inventory_items.append([item, 99 if not group + 1 == groups else
                                                # inventory[item] % 99])
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
