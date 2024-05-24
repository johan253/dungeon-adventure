import sys

import pygame
import pickle
import View.Tile as Tile
import View.Battle as Battle
from View.Button import Button
from controller.DungeonAdventure import DungeonAdventure
from model.DugeonRoom import DungeonRoom
from model.RoomItem import RoomItem
from View.MainMenu import main_menu

pygame.init()
DIFFICULTY = 3
WIDTH = 1280
HEIGHT = 720
__GAME: DungeonAdventure | None = None
MAX_TILE_SIZE = 96
REDUCTION_FACTOR_PER_DIFFICULTY = 8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pause = False


def play(screen, game):
    global SCREEN
    SCREEN = screen
    __gameplay(game)


def save_game_state(game_state):
    with open("saved_game.pkl", "wb") as file:
        pickle.dump(game_state, file)


def load_game_state():
    try:
        with open("saved_game.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None


def get_font(size):
    return pygame.font.Font('Assets/Dungeon Depths.ttf', size)


def draw_pause():
    pause_mouse_position = pygame.mouse.get_pos()

    pause_height = 640
    pause_width = 360

    button_radius = 10

    pygame.draw.rect(SCREEN, (128, 128, 128, 128), [0, 100, pause_width, pause_height])
    pause_text = get_font(15).render("GAME PAUSED: TO RESUME PRESS ''ESC'' or ''P''", True, 'blue')
    pause_rect = pause_text.get_rect(center=(640, 50))
    SCREEN.blit(pause_text, pause_rect)

    save_button_rect = pygame.Rect(30, 150, 600, 50)
    restart_button_rect = pygame.Rect(30, 250, 600, 50)
    main_menu_button_rect = pygame.Rect(30, 350, 600, 50)
    close_game_button_rect = pygame.Rect(30, 450, 600, 50)
    inventory_button_rect = pygame.Rect(30, 550, 600, 50)

    # Change color based on mouse position
    save_color = 'red' if save_button_rect.collidepoint(pause_mouse_position) else 'blue'
    restart_color = 'red' if restart_button_rect.collidepoint(pause_mouse_position) else 'blue'
    main_menu_color = 'red' if main_menu_button_rect.collidepoint(pause_mouse_position) else 'blue'
    close_game_color = 'red' if close_game_button_rect.collidepoint(pause_mouse_position) else 'blue'
    inventory_color = 'red' if inventory_button_rect.collidepoint(pause_mouse_position) else 'blue'

    # Draw buttons
    save_button_text = get_font(15).render('Save', True, save_color)
    restart_button_text = get_font(15).render('Restart', True, restart_color)
    main_menu_button_text = get_font(15).render('Main Menu', True, main_menu_color)
    close_game_button_text = get_font(15).render('Close Game', True, close_game_color)
    inventory_button_text = get_font(15).render('Inventory', True, inventory_color)

    SCREEN.blit(save_button_text, (30, 165))
    SCREEN.blit(restart_button_text, (30, 265))
    SCREEN.blit(main_menu_button_text, (30, 365))
    SCREEN.blit(close_game_button_text, (30, 465))
    SCREEN.blit(inventory_button_text, (30, 575))

    pygame.display.update()

    return save_button_rect, restart_button_rect, main_menu_button_rect, close_game_button_rect, inventory_button_rect


def __gameplay(game: DungeonAdventure):
    global __GAME, pause, restart, save, main_menu_button, close_game, inventory
    global SCREEN
    __GAME = game
    title_text = pygame.font.Font("Assets/Dungeon Depths.ttf", 12).render("Dungeon Adventure", True, (255, 0, 0))
    title_text_rect = title_text.get_rect(center=(SCREEN.get_width() // 2, title_text.get_height() // 2))
    SCREEN.fill("black")
    SCREEN.blit(title_text, title_text_rect)
    tile_size = MAX_TILE_SIZE - (REDUCTION_FACTOR_PER_DIFFICULTY * (DIFFICULTY - 1))
    dungeon_width = tile_size * game.get_dungeon().get_dimensions()[0]
    dungeon_height = tile_size * game.get_dungeon().get_dimensions()[1]
    dungeon_starting_x = (SCREEN.get_width() - dungeon_width) // 2
    dungeon_starting_y = (SCREEN.get_height() - dungeon_height) // 2
    draw_dungeon(SCREEN, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                 dungeon_starting_y // tile_size)
    while True:
        pygame.display.set_caption('DUNGEON ADVENTURE')
        if pause:
            save, restart, main_menu_button, close_game, inventory = draw_pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if pause and event.type == pygame.MOUSEBUTTONDOWN:
                if save.collidepoint(event.pos):
                    save_game_state(__GAME)
                if restart.collidepoint(event.pos):
                    pass
                if main_menu_button.collidepoint(event.pos):
                    pause = False
                    main_menu()
                if close_game.collidepoint(event.pos):
                    sys.exit()
                if inventory.collidepoint(event.pos):
                    pass
            if event.type == pygame.KEYDOWN:
                if not pause:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        game.move_player("north")
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        game.move_player("south")
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        game.move_player("west")
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        game.move_player("east")
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause = not pause
                if game.get_battle_state():
                    # Battle.start(game)
                    pass
                SCREEN.fill("black")
                draw_dungeon(SCREEN, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                             dungeon_starting_y // tile_size)
                print(f"current inventoryL {game.get_inventory()}")
        pygame.display.flip()
        pygame.time.delay(1000 // 60)


def draw_dungeon(screen: pygame.Surface, dungeon, room_size, x, y):
    root = dungeon.get_root()
    draw_room(screen, root, x, y, room_size, set())


def draw_room(screen: pygame.Surface, room: DungeonRoom, x, y, room_size, visited):
    if room is None or room in visited or room not in __GAME.get_visited_rooms():
        return
    visited.add(room)
    mini_tile_size = room_size // 3
    for i in range(3):
        for j in range(3):
            tile = __get_appropriate_tile(room, j, i, mini_tile_size)
            screen.blit(tile, (x * room_size + i * mini_tile_size, y * room_size + j * mini_tile_size))
    for dx, dy, direction in [(1, 0, room.get_east()), (0, 1, room.get_south()), (-1, 0, room.get_west()),
                              (0, -1, room.get_north())]:
        if direction:
            # pygame.draw.line(screen, (0, 255, 0),
            #                  (x * room_size + room_size // 2, y * room_size + room_size // 2),
            #                  ((x + dx) * room_size + room_size // 2, (y + dy) * room_size + room_size // 2))
            draw_room(screen, direction, x + dx, y + dy, room_size, visited)


def __get_appropriate_tile(room: DungeonRoom, row, col, size):
    if row == 0 and col == 0:
        return Tile.get_tile(Tile.WALL_CORNER_NW, size, size)
    elif row == 0 and col == 2:
        return Tile.get_tile(Tile.WALL_CORNER_NE, size, size)
    elif row == 2 and col == 0:
        return Tile.get_tile(Tile.WALL_CORNER_SW, size, size)
    elif row == 2 and col == 2:
        return Tile.get_tile(Tile.WALL_CORNER_SE, size, size)
    elif row == 0:
        return Tile.get_tile(Tile.WALL_UP, size, size) if not room.get_north() else Tile.get_tile(Tile.FLOOR, size,
                                                                                                  size)
    elif row == 2:
        return Tile.get_tile(Tile.WALL_DOWN, size, size) if not room.get_south() else Tile.get_tile(Tile.FLOOR, size,
                                                                                                    size)
    elif col == 0:
        return Tile.get_tile(Tile.WALL_LEFT, size, size) if not room.get_west() else Tile.get_tile(Tile.FLOOR, size,
                                                                                                   size)
    elif col == 2:
        return Tile.get_tile(Tile.WALL_RIGHT, size, size) if not room.get_east() else Tile.get_tile(Tile.FLOOR, size,
                                                                                                    size)
    elif room == __GAME.get_current_room():
        char_name = type(__GAME.get_player()).__name__
        return Tile.get_tile(Tile.PLAYER[char_name], size, size)
    elif room is __GAME.get_dungeon().get_exit():
        return Tile.get_tile(Tile.EXIT, size, size)
    else:
        return Tile.get_tile(Tile.FLOOR, size, size)
