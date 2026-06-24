import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT, LAYERS, PLAYER_TOOL_OFFSET
from utils.math_utils import Vector2

class Camera:
    def __init__(self, group: pygame.sprite.Group):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.group = group
        self.offset = Vector2()

    def custom_draw(self, player):
        # Shifting
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            # print(layer)
            for sprite in sorted(self.group.sprites(), key=lambda sprite_: sprite_.rect.centery):  # sorted for overlap
                if sprite.z == layer:  # to make the correct order
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
