import pygame
from model.CharacterFactory import CharacterFactory

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
MONSTER = {
    CharacterFactory.GREMLIN: (1, 2),
    CharacterFactory.OGRE: (2, 2),
    CharacterFactory.SKELETON: (3, 2),

}
HEALING_POTION = (4, 2)
VISION_POTION = (5, 2)
PIT = (6, 2)
MULTIPLE_ITEMS = (7, 2)
PILLAR_A = (0, 3)
PILLAR_E = (1, 3)
PILLAR_I = (2, 3)
PILLAR_P = (3, 3)
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
    """
    Getter for the tiles of the dungeon.
    :param tile_type: The tile type to be obtained.
    :param width: Width value of the tiles
    :param height: Height value of the tile
    :return: The image of the tile
    """
    image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    image.blit(TILE_SHEET, (0, 0), (tile_type[0] * TILE_SIZE, tile_type[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    image = pygame.transform.scale(image, (width, height))
    return image


