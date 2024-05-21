import pygame
import sys

from src.View.MainMenu import Screen
from src.controller.DungeonAdventure import DungeonAdventure


def start(game: DungeonAdventure):
    """
    This method starts the battle sequence for the Dungeon Adventure game.
    :param game: The game object
    """
    Screen.fill((122, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        pygame.time.delay(1000 // 60)
