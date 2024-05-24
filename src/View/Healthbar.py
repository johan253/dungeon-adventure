import pygame
from src.model.DungeonCharacter import DungeonCharacter


class Healthbar:
    def __init__(self, player: DungeonCharacter):
        self.__player: DungeonCharacter = player

    def draw(self, screen: pygame.Surface, coordinates: tuple[int, int] = (0, 0), size: tuple[int, int] = (100, 10)):
        x, y = coordinates
        width, height = size
        damaged = self.__player.get_health() / self.__player.get_max_health()
        pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height))
        pygame.draw.rect(screen, (0, 255, 0), (x, y, width * damaged, height))
        pygame.draw.rect(screen, (0, 0, 0), (x, y, width, height), 1)
