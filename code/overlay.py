import pygame

from support import import_img
from settings import *


class Overlay:
    def __init__(self, player):
        # General setup
        self.display_surface = pygame.display.get_surface()
        self.player = player

        # imports
        overlay_path = "../graphics/overlay"
        self.tools_surf = {tool: import_img(f"{overlay_path}/{tool}.png").convert_alpha()
                           for tool in player.tools}
        self.seeds_surf = {seed: pygame.transform.scale(import_img(f"{overlay_path}/{seed} seed.png").convert_alpha(),
                                                        (46, 54)) for seed in player.seeds}

    def display(self):
        # Tools
        tool_surf = self.tools_surf[self.player.selected_tool]
        tool_rect = tool_surf.get_rect(midbottom=OVERLAY_POSITIONS['tool'])
        self.display_surface.blit(tool_surf, tool_rect)  # dest is the place of the item

        # Seeds
        seed_surf = self.seeds_surf[self.player.selected_seed]
        seed_rect = seed_surf.get_rect(midbottom=OVERLAY_POSITIONS['seed'])
        self.display_surface.blit(seed_surf, seed_rect)
