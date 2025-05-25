from random import choice

from settings import *
from pytmx.util_pygame import load_pygame
from support import *


class SoilTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil']


class WaterTile(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        # noinspection PyTypeChecker
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)
        self.z = LAYERS['soil water']


class Plant(pygame.sprite.Sprite):
    def __init__(self, plant_type, groups, soil, check_watered):
        # noinspection PyTypeChecker
        super().__init__(groups)

        # Setup
        self.plant_type = plant_type
        self.frames = import_folder(f'../graphics/fruit/{plant_type}')
        self.soil = soil
        self.check_watered = check_watered

        # Plant growing
        self.age = 0
        self.max_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[plant_type]
        self.harvestable = False

        # Sprite setup
        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == 'corn' else -8  # they are different in size
        self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['ground plant']

    def display(self):
        if int(self.age) > 0:
            self.z = LAYERS['main']
            self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

        if self.age >= self.max_age:
            self.age = self.max_age
            self.harvestable = True

        self.image = self.frames[int(self.age)]
        self.rect = self.image.get_rect(midbottom=self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))

    def grow(self):
        if self.check_watered(self.rect.center):
            self.age += self.grow_speed

            self.display()


class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        # Sprite groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.plant_sprites = pygame.sprite.Group()

        # Graphics
        self.soil_surfs = import_folder_dict("../graphics/soil")
        self.water_surfs = import_folder("../graphics/soil_water")

        self.create_soil_grid()
        self.create_hit_rects()

        # Sounds
        self.hoe_sound = import_audio("../audio/hoe.wav")
        self.hoe_sound.set_volume(0.1)

        self.plant_sound = import_audio("../audio/plant.wav")
        self.plant_sound.set_volume(0.2)

    # Requirements
    def create_soil_grid(self):
        ground = import_img("../graphics/world/ground.png")  # Not shown to the player
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.grid = [[{"Soil info": {"Farmable": False, "Hit": False, "Watered": False},
                       "Planting info": {"Planted": False, "Seed": None, "Age": 0}}
                      for _ in range(h_tiles)] for _ in range(v_tiles)]
        # surf is not important, y row, x col, [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        # noinspection PyUnresolvedReferences
        for x, y, _ in load_pygame(get_resource_path("../data/map.tmx")).get_layer_by_name('Farmable').tiles():
            # noinspection PyTypeChecker
            self.grid[y][x]["Soil info"]["Farmable"] = True

    def create_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if cell['Soil info']['Farmable']:
                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE
                    rect = pygame.Rect((x, y), (TILE_SIZE, TILE_SIZE))
                    self.hit_rects.append(rect)

    def get_hit(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()

                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE

                if self.grid[y][x]["Soil info"]["Farmable"]:
                    self.grid[y][x]["Soil info"]["Hit"] = True
                    self.create_soil_tiles()
                    # noinspection PyUnresolvedReferences
                    if self.raining:
                        self.water_all()

    def water(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                # noinspection PyTypeChecker
                self.grid[y][x]["Soil info"]["Watered"] = True

                self.water_tile(soil_sprite)

    def water_all(self):
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if cell["Soil info"]["Hit"] and not cell["Soil info"]["Watered"]:
                    cell["Soil info"]["Watered"] = True

                    x = index_col * TILE_SIZE
                    y = index_row * TILE_SIZE

                    surf = choice(self.water_surfs)
                    # noinspection PyTypeChecker
                    WaterTile((x, y), surf, [self.all_sprites, self.water_sprites])

    def water_tile(self, soil_sprite):
        pos = soil_sprite.rect.topleft
        surf = choice(self.water_surfs)
        # noinspection PyTypeChecker
        WaterTile(pos, surf, [self.all_sprites, self.water_sprites])

    def remove_water(self):
        # Destroy water sprites
        for sprite in self.water_sprites.sprites():
            sprite.kill()

        # Clean up the grid
        for row in self.grid:
            for cell in row:
                if cell["Soil info"]["Watered"]:
                    cell["Soil info"]["Watered"] = False

    def check_watered(self, pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.grid[y][x]
        is_watered = cell["Soil info"]["Watered"]
        return is_watered

    def plant_seed(self, target_pos, seed):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                self.plant_sound.play()

                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE

                if not self.grid[y][x]["Planting info"]["Planted"]:
                    # noinspection PyTypeChecker
                    self.grid[y][x]["Planting info"]["Planted"] = True
                    self.grid[y][x]["Planting info"]["Seed"] = seed
                    # noinspection PyTypeChecker
                    Plant(seed, [self.all_sprites, self.plant_sprites, self.collision_sprites], soil_sprite,
                          self.check_watered)
                    self.planted = True
                    return
        self.planted = False

    def plant_seeds(self):
        for soil_sprite in self.soil_sprites.sprites():
            x = soil_sprite.rect.x // TILE_SIZE
            y = soil_sprite.rect.y // TILE_SIZE
            cell = self.grid[y][x]
            if cell["Soil info"]["Watered"]:
                self.water_tile(soil_sprite)

            if cell["Planting info"]["Planted"]:
                # noinspection PyTypeChecker
                plant = Plant(cell["Planting info"]["Seed"],
                              [self.all_sprites, self.plant_sprites, self.collision_sprites],
                              soil_sprite, self.check_watered)
                plant.age = cell["Planting info"]["Age"]
                plant.display()

    def update_plants(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

            # Save the data to the grid
            x = plant.soil.rect.left // TILE_SIZE
            y = plant.soil.rect.top // TILE_SIZE
            cell = self.grid[y][x]
            cell["Planting info"]["Age"] = plant.age

    def create_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.grid):
            for index_col, cell in enumerate(row):
                if cell["Soil info"]["Hit"]:
                    # Tile options
                    t = self.grid[index_row - 1][index_col]["Soil info"]["Hit"]
                    b = self.grid[index_row + 1][index_col]["Soil info"]["Hit"]
                    r = row[index_col + 1]["Soil info"]["Hit"]
                    l = row[index_col - 1]["Soil info"]["Hit"]

                    tile_type = "o"

                    # All sides
                    if all((t, b, r, l)):
                        tile_type = "x"

                    # Horizontal tiles only
                    if l and not any((t, r, b)):
                        tile_type = "r"
                    if r and not any((t, l, b)):
                        tile_type = "l"
                    if r and l and not any((t, b)):
                        tile_type = "lr"

                    # Vertical tiles only
                    if t and not any((r, l, b)):
                        tile_type = "b"
                    if b and not any((r, l, t)):
                        tile_type = "t"
                    if t and b and not any((r, l)):
                        tile_type = "tb"

                    # Corner
                    if l and b and not any((r, t)):
                        tile_type = "tr"
                    if r and b and not any((l, t)):
                        tile_type = "tl"
                    if l and t and not any((r, b)):
                        tile_type = "br"
                    if r and t and not any((l, b)):
                        tile_type = "bl"

                    # T shapes
                    if all((r, t, b)) and not l:
                        tile_type = "tbr"
                    if all((l, t, b)) and not r:
                        tile_type = "tbl"
                    if all((r, l, b)) and not t:
                        tile_type = "lrt"
                    if all((r, l, t)) and not b:
                        tile_type = "lrb"

                    # Add more logic

                    # noinspection PyTypeChecker
                    SoilTile((index_col * TILE_SIZE, index_row * TILE_SIZE), self.soil_surfs[tile_type],
                             sorted([self.all_sprites, self.soil_sprites], key=lambda group: len(group.sprites())))
