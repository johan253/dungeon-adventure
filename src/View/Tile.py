import pygame
from src.model.CharacterFactory import CharacterFactory

FLOOR = (4, 0)
WALL_LEFT = (2, 1)
WALL_RIGHT = (3, 1)
WALL_UP = (0, 1)
WALL_DOWN = (1, 1)
WALL_CORNER_NW = (3, 0)
WALL_CORNER_NE = (0, 0)
WALL_CORNER_SW = (2, 0)
WALL_CORNER_SE = (1, 0)
PLAYER = {
    CharacterFactory.WARRIOR: (4, 1),
    CharacterFactory.THIEF: (5, 1),
    CharacterFactory.PRIESTESS: (6, 1),
}
EXIT = (0, 2)

INVENTORY_HEALING_POTION = (0, 4)
INVENTORY_VISION_POTION = (1, 4)
INVENTORY_PILLAR_A = (2, 4)
INVENTORY_PILLAR_E = (2, 5)
INVENTORY_PILLAR_I = (2, 6)
INVENTORY_PILLAR_P = (2, 7)

TILE_SIZE = 8
TILE_SHEET = pygame.image.load("Assets/tiles.png")


def get_tile(tile_type: tuple[int, int], width: int, height: int):
    image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    image.blit(TILE_SHEET, (0, 0), (tile_type[0] * TILE_SIZE, tile_type[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    image = pygame.transform.scale(image, (width, height))
    return image


