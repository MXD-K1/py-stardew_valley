import pygame

from managers.resource_manager import resource_manager
from utils.load_utils import load_sound
from utils.logging_config import getLogger

logger = getLogger(__name__)


def load_sounds() -> None:
    try:
        sound_1 = load_sound("assets/audio/success.wav")
        sound_1.set_volume(0.3)
        sound_2 = load_sound("assets/audio/music.mp3")
        sound_3 = load_sound("assets/audio/water.mp3")
        sound_3.set_volume(0.2)
        sound_4 = load_sound("assets/audio/axe.mp3")
    except pygame.error as e:
        logger.exception(e)
        raise
    else:
        resource_manager.add_sound("success", sound_1)
        resource_manager.add_sound("bg_music", sound_2)
        resource_manager.add_sound("watering", sound_3)
        resource_manager.add_sound("axe", sound_4)

        logger.info("Sounds loaded successfully")
