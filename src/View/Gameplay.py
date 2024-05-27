import pickle
import sys

import pygame

import View.Tile as Tile
from View.Healthbar import Healthbar
from View.MainMenu import main_menu
from controller.DungeonAdventure import DungeonAdventure
from model.DugeonRoom import DungeonRoom
from src.model.Ogre import Ogre
from src.model.Skeleton import Skeleton
from src.model.Gremlin import Gremlin

pygame.init()
DIFFICULTY = 3
WIDTH = 1280
HEIGHT = 720
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
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

    pygame.draw.rect(SCREEN, 'black', [0, 100, pause_width, pause_height])
    pause_text = get_font(15).render("GAME PAUSED: TO RESUME PRESS ''ESC'' or ''P''", True, 'yellow')
    pause_rect = pause_text.get_rect(center=(640, 50))
    SCREEN.blit(pause_text, pause_rect)

    save_button_rect = pygame.Rect(30, 130, pause_width - 30, 50)
    restart_button_rect = pygame.Rect(30, 230, pause_width - 30, 50)
    main_menu_button_rect = pygame.Rect(30, 330, pause_width - 30, 50)
    close_game_button_rect = pygame.Rect(30, 430, pause_width - 30, 50)
    help_button_rect = pygame.Rect(30, 530, pause_width - 30, 50)

    # Change color based on mouse position
    save_color = 'red' if save_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    restart_color = 'red' if restart_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    main_menu_color = 'red' if main_menu_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    close_game_color = 'red' if close_game_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    help_color = 'red' if help_button_rect.collidepoint(pause_mouse_position) else 'yellow'

    # Draw buttons
    save_button_text = get_font(15).render('Save', True, save_color)
    restart_button_text = get_font(15).render('Restart', True, restart_color)
    main_menu_button_text = get_font(15).render('Main Menu', True, main_menu_color)
    close_game_button_text = get_font(15).render('Close Game', True, close_game_color)
    help_button_text = get_font(15).render('Help', True, help_color)

    SCREEN.blit(save_button_text, (30, 130))
    SCREEN.blit(restart_button_text, (30, 230))
    SCREEN.blit(main_menu_button_text, (30, 330))
    SCREEN.blit(close_game_button_text, (30, 430))
    SCREEN.blit(help_button_text, (30, 530))

    pygame.display.update()

    return save_button_rect, restart_button_rect, main_menu_button_rect, close_game_button_rect, help_button_rect


def draw_help():
    global SCREEN
    pygame.init()  # Initialize Pygame
    help_height = 650
    help_width = 660
    help_surface = pygame.Surface((help_width, help_height))
    help_surface.fill('black')

    text = ("""          To escape:\n
        1.Collect all 4 pillars of oop:\n
            a.Pillar of abstraction
            b.Pillar of Encapsulation
            c.pillar of inheritance
            d.pillar of polymorphism\n
        2.be alive\n
        
        the user will encounter the following:\n
        1.Monsters(they hit back)
        2.pits
        3.potions\n\n
        
        good luck adventurer!!""")

    help_font = pygame.font.SysFont(None, 20)
    y_offset = 30
    for line in text.split('\n'):
        help_text = get_font(10).render(line, True, 'red')
        text_rect = help_text.get_rect(center=(200, y_offset))
        help_surface.blit(help_text, text_rect)
        y_offset += text_rect.height + 1

    SCREEN.blit(help_surface, (400, 80))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    SCREEN.fill('black')
                    pygame.display.update()
                    return


def __gameplay(game: DungeonAdventure):
    global __GAME, pause, restart, save, main_menu_button, close_game, help_option
    global SCREEN
    __GAME = game
    health_text = pygame.font.Font("Assets/Dungeon Depths.ttf", 12).render("Health", True, (255, 255, 255))
    title_text_rect = health_text.get_rect(center=(SCREEN.get_width() // 2, health_text.get_height() + 685))
    tile_size = MAX_TILE_SIZE - (REDUCTION_FACTOR_PER_DIFFICULTY * (DIFFICULTY - 1))
    dungeon_width = tile_size * game.get_dungeon().get_dimensions()[0]
    dungeon_height = tile_size * game.get_dungeon().get_dimensions()[1]
    dungeon_starting_x = (SCREEN.get_width() - dungeon_width) // 2
    dungeon_starting_y = (SCREEN.get_height() - dungeon_height) // 2 + tile_size
    SCREEN.fill("black")
    draw_dungeon(SCREEN, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                 dungeon_starting_y // tile_size)

    healthbar_width = SCREEN.get_width() // 3
    healthbar_height = 48
    healthbar_starting_x = healthbar_width + 10
    healthbar_starting_y = health_text.get_height() + 625
    healthbar = Healthbar(game.get_player())
    SCREEN.blit(health_text, title_text_rect)
    while True:
        pygame.display.set_caption('DUNGEON ADVENTURE')
        if not pause:
            healthbar.draw(SCREEN, (healthbar_starting_x, healthbar_starting_y), (healthbar_width, healthbar_height))
        if pause:
            pygame.display.set_caption('PAUSE')
            save, restart, main_menu_button, close_game, help_option = draw_pause()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pause:
                if save.collidepoint(event.pos):
                    save_game_state(__GAME)
                if restart.collidepoint(event.pos):
                    pass
                if main_menu_button.collidepoint(event.pos):
                    pause = False
                    main_menu()
                if close_game.collidepoint(event.pos):
                    sys.exit()
                if help_option.collidepoint(event.pos):
                    draw_help()
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
                    elif event.key == pygame.K_x:
                        game.get_player().damage(10)
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause = not pause
                if game.get_battle_state():
                    # Battle.start(game)
                    pass
                SCREEN.fill("black")
                SCREEN.blit(health_text, title_text_rect)
                draw_dungeon(SCREEN, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                             dungeon_starting_y // tile_size)
                healthbar.draw(SCREEN, (healthbar_starting_x, healthbar_starting_y),
                               (healthbar_width, healthbar_height))
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
