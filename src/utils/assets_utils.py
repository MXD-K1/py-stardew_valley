from pygame.transform import scale as scale_image
from pygame.transform import flip as flip_image

def invert_color(color):
    return 255 - color[0], 255 - color[1], 255 - color[2]

__all__ = ["scale_image", "flip_image", "invert_color"]
