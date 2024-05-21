import sys

import pygame

import Tile
from SaveLoadManager import SaveLoadSystem
from View.Button import Button
from View.MainMenu import get_font, Screen
from controller.DungeonAdventure import DungeonAdventure
from model.DugeonRoom import DungeonRoom

save_data = SaveLoadSystem(".save", "saved_data")
DIFFICULTY = 1


def play(game):
    __gameplay(game)


def __gameplay(game: DungeonAdventure):
    title_text = get_font(12).render("Dungeon Adventure", True, (0, 255, 0))
    title_text_rect = title_text.get_rect(center=(Screen.get_width() // 2, title_text.get_height() // 2))
    Screen.fill("black")
    Screen.blit(title_text, title_text_rect)
    tile_size = 96 - (8 * (DIFFICULTY - 1))
    dungeon_width = tile_size * game.get_dungeon().get_dimensions()[0]
    dungeon_height = tile_size * game.get_dungeon().get_dimensions()[1]
    dungeon_starting_x = (Screen.get_width() - dungeon_width) // 2
    dungeon_starting_y = (Screen.get_height() - dungeon_height) // 2
    print(dungeon_starting_x, dungeon_starting_y)
    draw_dungeon(Screen, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size, dungeon_starting_y // tile_size)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
        pygame.time.delay(1000 // 60)


def draw_dungeon(screen: pygame.Surface, dungeon, room_size, x, y):
    root = dungeon.get_root()
    draw_room(screen, root, x, y, room_size, set())


def __get_appropriate_tile(room, row, col, size):
    if row == 0 and col == 0:
        return Tile.get_tile(Tile.WALL_CORNER_NW, size, size)
    elif row == 0 and col == 2:
        return Tile.get_tile(Tile.WALL_CORNER_NE, size, size)
    elif row == 2 and col == 0:
        return Tile.get_tile(Tile.WALL_CORNER_SW, size, size)
    elif row == 2 and col == 2:
        return Tile.get_tile(Tile.WALL_CORNER_SE, size, size)
    elif row == 0:
        return Tile.get_tile(Tile.WALL_UP, size, size) if not room.get_north() else Tile.get_tile(Tile.FLOOR, size, size)
    elif row == 2:
        return Tile.get_tile(Tile.WALL_DOWN, size, size) if not room.get_south() else Tile.get_tile(Tile.FLOOR, size, size)
    elif col == 0:
        return Tile.get_tile(Tile.WALL_LEFT, size, size) if not room.get_west() else Tile.get_tile(Tile.FLOOR, size, size)
    elif col == 2:
        return Tile.get_tile(Tile.WALL_RIGHT, size, size) if not room.get_east() else Tile.get_tile(Tile.FLOOR, size, size)
    else:
        return Tile.get_tile(Tile.FLOOR, size, size)


def draw_room(screen: pygame.Surface, room: DungeonRoom, x, y, room_size, visited):
    if room is None or room in visited:
        return
    visited.add(room)
    mini_tile_size = room_size // 3
    for i in range(3):
        for j in range(3):
            tile = __get_appropriate_tile(room, j, i, mini_tile_size)
            screen.blit(tile, (x * room_size + i * mini_tile_size, y * room_size + j * mini_tile_size))
    for dx, dy, direction in [(1, 0, room.get_east()), (0, 1, room.get_south()), (-1, 0, room.get_west()), (0, -1, room.get_north())]:
        if direction:
            pygame.draw.line(screen, (0, 255, 0),
                             (x * room_size + room_size // 2, y * room_size + room_size // 2),
                             ((x + dx) * room_size + room_size // 2, (y + dy) * room_size + room_size // 2))
            draw_room(screen, direction, x + dx, y + dy, room_size, visited)

    # tile = Tile.get_tile(Tile.FLOOR, room_size, room_size)
    # Screen.blit(tile, (x * room_size, y * room_size))
    # room_char = " " if len(room.get_items()) == 0 else room.get_items()[0].value
    # if len(room.get_items()) > 1:
    #     room_char = "M"
    # screen.blit(get_font(10).render(f"{room_char}", True, (0, 255, 0)),
    #             (x * room_size + room_size // 2, y * room_size + room_size // 2))
    #
    # # Draw a line to the room to the east
    # if room.get_east():
    #     pygame.draw.line(screen, (0, 255, 0),
    #                      (x * room_size + room_size // 2, y * room_size + room_size // 2),
    #                      ((x + 1) * room_size + room_size // 2, y * room_size + room_size // 2))
    #     draw_room(screen, room.get_east(), x + 1, y, room_size, visited)
    #
    # # Draw a line to the room to the south
    # if room.get_south():
    #     pygame.draw.line(screen, (0, 255, 0),
    #                      (x * room_size + room_size // 2, y * room_size + room_size // 2),
    #                      (x * room_size + room_size // 2, (y + 1) * room_size + room_size // 2))
    #     draw_room(screen, room.get_south(), x, y + 1, room_size, visited)
    #
    # if room.get_west():
    #     pygame.draw.line(screen, (0, 255, 0),
    #                      (x * room_size + room_size // 2, y * room_size + room_size // 2),
    #                      ((x - 1) * room_size + room_size // 2, y * room_size + room_size // 2))
    #     draw_room(screen, room.get_west(), x - 1, y, room_size, visited)
    #
    # if room.get_north():
    #     pygame.draw.line(screen, (0, 255, 0),
    #                      (x * room_size + room_size // 2, y * room_size + room_size // 2),
    #                      (x * room_size + room_size // 2, (y - 1) * room_size + room_size // 2))
    #     draw_room(screen, room.get_north(), x, y - 1, room_size, visited)