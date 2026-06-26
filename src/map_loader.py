import pygame

from entities.player import Player
from config import TILE_SIZE, LAYERS
from sprites import Interaction, Generic, Tree, Water, WildFlower
from utils.load_utils import load_map, load_image, load_folder_of_images


class MapLoader:
    def __init__(self, all_sprites, collision_sprites, tree_sprites, interaction_sprites, player_add, soil_layer, toggle_shop):
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.tree_sprites = tree_sprites
        self.interaction_sprites = interaction_sprites

        self.player_add = player_add
        self.soil_layer = soil_layer
        self.toggle_shop = toggle_shop

    def clear_groups(self):
        self.all_sprites.clear()
        self.collision_sprites.clear()
        self.tree_sprites.clear()
        self.interaction_sprites.clear()

    # noinspection PyTypeChecker PyUnresolvedReferences
    def load_map(self, map_path):
        map_data = load_map(map_path)

        # House
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:  # they must be in order
            for x, y, surf in map_data.get_layer_by_name(layer).tiles():
                # noinspection PyTypeChecker
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:  # they must be in order
            for x, y, surf in map_data.get_layer_by_name(layer).tiles():
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house top'])
                # A problem in the order rain house

        # Fence
        for x, y, surf in map_data.get_layer_by_name('Fence').tiles():
            # noinspection PyTypeChecker
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Water
        water_frames = load_folder_of_images("assets/graphics/water")
        for x, y, surf in map_data.get_layer_by_name('Water').tiles():
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Trees
        for obj in map_data.get_layer_by_name('Trees'):
            Tree(pos=(obj.x, obj.y),
                 surf=obj.image,
                 groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                 name=obj.name,
                 player_add=self.player_add)

        # Wild flowers
        for obj in map_data.get_layer_by_name('Decoration'):
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # Collision tiles
        for x, y, surf in map_data.get_layer_by_name('Collision').tiles():  # for x, y, surf these are tiles
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.surface.Surface((TILE_SIZE, TILE_SIZE)),
                    self.collision_sprites)

        # Player
        for obj in map_data.get_layer_by_name('Player'):
            if obj.name == "Start":
                self.player = Player(pos=(obj.x, obj.y),
                                     group=self.all_sprites,
                                     collision_sprites=self.collision_sprites,
                                     tree_sprites=self.tree_sprites,
                                     interaction=self.interaction_sprites,
                                     soil_layer=self.soil_layer,
                                     toggle_shop=self.toggle_shop)

            if obj.name == "Bed":
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

            if obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        Generic(pos=(0, 0),
                surf=load_image("assets/graphics/world/ground.png").convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['ground'])

        return self.player
