import pygame
from .core.game import Game


if __name__ == "__main__":
    game = Game()
    while game.running:
        game.update()
    pygame.quit()