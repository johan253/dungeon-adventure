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
    play_back_button = Button(image=None, position=(640, 460), text_input='Back', font=get_font(15),
                              color_1="white", color_2="grey")

    size = 5
    Screen.fill("black")
    while True:
        dungeon = game.get_dungeon()
        play_mouse_position = pygame.mouse.get_pos()

        play_back_button.change_color([play_back_button.x_position, play_back_button.y_position])
        play_back_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_data.save_data_from(game.get_game_data(), "saved_data")
                print("data saved")
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back_button.check_input(play_mouse_position):
                    Screen.fill("black")
                    draw_dungeon(Screen, dungeon, 64 - (8 * (DIFFICULTY - 1)), 4 - DIFFICULTY, 4 - DIFFICULTY)
                    size += 1
                    game.reset_dungeon(size)

        pygame.display.flip()


def draw_dungeon(screen: pygame.Surface, dungeon, room_size, x, y):
    root = dungeon.get_root()
    draw_room(screen, root, x, y, room_size, set())


def draw_room(screen: pygame.Surface, room: DungeonRoom, x, y, room_size, visited):
    if room in visited:
        return
    visited.add(room), visited
    # TODO: Get the appropriate tile for the room
    tile = Tile.get_tile(Tile.WALL_CORNER_NE, room_size, room_size)
    Screen.blit(tile, (x * room_size, y * room_size))
    room_char = " " if len(room.get_items()) == 0 else room.get_items()[0].value
    if len(room.get_items()) > 1:
        room_char = "M"
    screen.blit(get_font(10).render(f"{room_char}", True, (0, 255, 0)),
                (x * room_size + room_size // 2, y * room_size + room_size // 2))

    # Draw a line to the room to the east
    if room.get_east():
        pygame.draw.line(screen, (0, 255, 0),
                         (x * room_size + room_size // 2, y * room_size + room_size // 2),
                         ((x + 1) * room_size + room_size // 2, y * room_size + room_size // 2))
        draw_room(screen, room.get_east(), x + 1, y, room_size, visited)

    # Draw a line to the room to the south
    if room.get_south():
        pygame.draw.line(screen, (0, 255, 0),
                         (x * room_size + room_size // 2, y * room_size + room_size // 2),
                         (x * room_size + room_size // 2, (y + 1) * room_size + room_size // 2))
        draw_room(screen, room.get_south(), x, y + 1, room_size, visited)

    if room.get_west():
        pygame.draw.line(screen, (0, 255, 0),
                         (x * room_size + room_size // 2, y * room_size + room_size // 2),
                         ((x - 1) * room_size + room_size // 2, y * room_size + room_size // 2))
        draw_room(screen, room.get_west(), x - 1, y, room_size, visited)

    if room.get_north():
        pygame.draw.line(screen, (0, 255, 0),
                         (x * room_size + room_size // 2, y * room_size + room_size // 2),
                         (x * room_size + room_size // 2, (y - 1) * room_size + room_size // 2))
        draw_room(screen, room.get_north(), x, y - 1, room_size, visited)