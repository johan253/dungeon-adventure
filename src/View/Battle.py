import pygame
import sys

from src.controller.DungeonAdventure import DungeonAdventure


def start(screen, game: DungeonAdventure):
    """
    This method starts the battle sequence for the Dungeon Adventure game.
    :param screen: The screen to draw the battle
    :param game: The game object
    """
    screen.fill((122, 255, 255))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        pygame.time.delay(1000 // 60)
