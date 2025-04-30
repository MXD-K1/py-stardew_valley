from random import randint

from pytmx.util_pygame import load_pygame

from settings import *
from player import Player
from overlay import Overlay
from sprites import Generic, Water, WildFlower, Tree, Interaction, Particle
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from menu import Menu


class Level:
    def __init__(self):

        # Get display surface above the black screen
        self.display_surface = pygame.display.get_surface()

        # Sprite groups
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)

        # Sky
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # Shop
        self.menu = Menu(self.player, self.toggle_shop)
        self.shop_active = False

        # Sound (music)
        self.success = pygame.mixer.Sound("../audio/success.wav")
        self.success.set_volume(0.3)
        self.music = pygame.mixer.Sound("../audio/music.mp3")
        self.music.play(loops=-1)  # inf

    # noinspection PyUnresolvedReferences,PyTypeChecker
    def setup(self):
        # the map
        tmx_data = load_pygame('../data/map.tmx')

        # house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:  # they must be in order
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                # noinspection PyTypeChecker
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

        for layer in ['HouseWalls', 'HouseFurnitureTop']:  # they must be in order
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                # noinspection PyTypeChecker
                Generic((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, LAYERS['house top'])
                # A problem in the oder rain house

        # Fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            # noinspection PyTypeChecker
            Generic((x * TILE_SIZE, y * TILE_SIZE), surf, [self.all_sprites, self.collision_sprites])

        # Water
        water_frames = import_folder("../graphics/water")
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            # noinspection PyTypeChecker
            Water((x * TILE_SIZE, y * TILE_SIZE), water_frames, self.all_sprites)

        # Trees
        for obj in tmx_data.get_layer_by_name('Trees'):
            # noinspection PyTypeChecker
            Tree(pos=(obj.x, obj.y),
                 surf=obj.image,
                 groups=[self.all_sprites, self.collision_sprites, self.tree_sprites],
                 name=obj.name,
                 player_add=self.player_add)

        # Wild flowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            # noinspection PyTypeChecker
            WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # Collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():  # for x, y, surf these are tiles
            Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.surface.Surface((TILE_SIZE, TILE_SIZE)),
                    self.collision_sprites)

        # Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == "Start":
                self.player = Player(pos=(obj.x, obj.y),
                                     group=self.all_sprites,
                                     collision_sprites=self.collision_sprites,
                                     tree_sprites=self.tree_sprites,
                                     interaction=self.interaction_sprites,
                                     soil_layer=self.soil_layer,
                                     toggle_shop= self.toggle_shop)

            if obj.name == "Bed":
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

            if obj.name == 'Trader':
                Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

        # noinspection PyTypeChecker
        Generic(pos=(0, 0),
                surf=pygame.image.load("../graphics/world/ground.png").convert_alpha(),
                groups=self.all_sprites,
                z=LAYERS['ground'])

    def player_add(self, item, amount=1):
        self.player.item_inventory[item] += amount

        self.success.play()

    def toggle_shop(self):
        self.shop_active = not self.shop_active

    def reset(self):
        # Plants
        self.soil_layer.update_plants()

        # Soil
        self.soil_layer.remove_water()

        # Randomize the rain
        self.raining = randint(0, 10) > 7
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        # Trees and apples
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            tree.create_fruit()

        # Sky
        self.sky.start_color = [255, 255, 255]

    def plant_collision(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites.sprites():
                if plant.harvestable and plant.rect.colliderect(self.player.hitbox):
                    self.player_add(plant.plant_type)
                    plant.kill()
                    # noinspection PyTypeChecker
                    Particle(plant.rect.topleft, plant.image, self.all_sprites, z=LAYERS['main'])

                    self.soil_layer.grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')

    def run(self, dt):
        # Drawing logic
        self.display_surface.fill("black")
        self.all_sprites.custom_draw(self.player)

        # Updates
        if self.shop_active:
            self.menu.update()
        else:
            self.all_sprites.update(dt)  # Call update in sprites
            self.plant_collision()

        # Weather
        self.overlay.display()
        # Weather -> Raining
        if self.raining and not self.shop_active:
            self.rain.update()

        # Daytime
        self.sky.display(dt)

        # Transition overlay
        if self.player.sleep:
            self.transition.play()


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        # Shifting
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            # print(layer)
            for sprite in sorted(self.sprites(), key=lambda sprite_: sprite_.rect.centery):  # sorted for overlap
                if sprite.z == layer:  # to make the correct order
                    # print(sprite, layer)
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)
                    # self.test_target_pos(sprite, player, offset_rect)

    def test_target_pos(self, sprite, player, offset_rect):
        """Not used in the project. Only for testing."""
        if sprite == player:
            pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
            hitbox_rect = player.hitbox.copy()
            hitbox_rect.center = offset_rect.center
            pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
            target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split("_")[0]]
            pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)
