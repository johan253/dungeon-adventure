import pygame

FLOOR = (4, 0)
WALL_HORIZONTAL = (0, 5)
WALL_VERTICAL = (1, 3)
WALL_CORNER_NW = (3, 3)
WALL_CORNER_NE = (4, 4)
WALL_CORNER_SW = (1, 4)
WALL_CORNER_SE = (0, 4)


TILE_SIZE = 8
SCALE = 8
TILE_SHEET = pygame.image.load("Assets/tiles.png")


def get_tile(tile_type: tuple[int, int], width: int, height: int):
    image = pygame.Surface((TILE_SIZE, TILE_SIZE))
    image.blit(TILE_SHEET, (0, 0), (tile_type[0] * TILE_SIZE, tile_type[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    image = pygame.transform.scale(image, (width, height))
    return image
