import pygame

from data.colors import COLORS
from data.constants import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from level import Level
from load_resources import load_sounds
from managers.resource_manager import resource_manager
from utils import quit_game
from utils.logging_config import setup_logging, getLogger

logger = None


class Game:
    def __init__(self) -> None:
        self._setup_game()
        self._setup_screen()
        self.level = Level()

    def _setup_game(self) -> None:
        pygame.init()
        self._load_resources()
        self.clock = pygame.time.Clock()

    @staticmethod
    def _load_resources() -> None:
        load_sounds()

    def _setup_screen(self) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Py-Stardew Valley")
        resource_manager.set_display_surf(self.screen)

    def handle_input_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.level.save_game_data()
                quit_game()

    def run(self) -> None:
        while True:
            self.handle_input_events()

            dt = self.clock.tick(FPS) / 1000
            self.level.run(dt)

            pygame.display.update()
            self.screen.fill(COLORS.BLACK)


def run_game() -> None:
    setup_logging()
    global logger
    logger = getLogger(__name__)

    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        quit_game()
    except Exception as e:
        logger.exception(e)
        raise


if __name__ == "__main__":
    run_game()
