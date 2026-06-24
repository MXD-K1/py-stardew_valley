import sys

import pygame

from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from level import Level
from utils import quit_game


class Game:
    def __init__(self):
        pygame.init()
        self._setup_screen()
        self.clock = pygame.time.Clock()
        self.level = Level()

    def _setup_screen(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Py-Stardew Valley")

    def handle_input_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.level.save_game_data()
                quit_game()

    def run(self):
        while True:
            self.handle_input_events()

            dt = self.clock.tick() / 1000
            self.level.run(dt)

            pygame.display.update()
            self.screen.fill("black")


def run_game():
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        quit_game()

if __name__ == "__main__":
    run_game()
