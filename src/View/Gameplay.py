import pickle
import sys
from collections import defaultdict

import pygame
import src.controller.DungeonEvent as DungeonEvent

import View.Tile as Tile
from View import Battle
from View import GameOver
from View.Button import Button
from View.Healthbar import Healthbar
from View.MainMenu import main_menu, get_font
from View.PlaySound import music, sound_efx
from controller.DungeonAdventure import DungeonAdventure
from model.DugeonRoom import DungeonRoom
from model.RoomItem import RoomItem

pygame.init()
DIFFICULTY = 0
WIDTH = 1280
HEIGHT = 720
SPRITE_WIDTH = 64
SPRITE_HEIGHT = 64
__GAME: DungeonAdventure | None = None
MAX_TILE_SIZE = 96
REDUCTION_FACTOR_PER_DIFFICULTY = 8
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SRCALPHA)
pause = False
LAST_FOUR_BUTTONS = []


def play(screen: pygame.Surface, game: DungeonAdventure) -> None:
    """
    This method starts the gameplay for the Dungeon Adventure game.
    :param screen: The screen to draw the gameplay
    :param game: The game object
    """
    global SCREEN, DIFFICULTY
    SCREEN = screen
    DIFFICULTY = game.get_dungeon().get_dimensions()[0] - 4
    __gameplay(game)


def save_game_state(game_state) -> None:
    """
    This method saves the game state to a file.
    :param game_state: The game state to save
    """
    with open("../saved_data/saved_game.pkl", "wb") as file:
        pickle.dump(game_state, file)


def load_game_state() -> DungeonAdventure | None:
    # TODO: Move this method to MainMenu.py
    """
    This method loads the game state from a file.
    :return: The game state
    """
    try:
        with open("../saved_data/saved_game.pkl", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return None


def draw_pause() -> tuple[pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect, pygame.Rect]:
    """
    This method draws the pause menu on the screen.
    :return: The buttons on the pause menu
    """
    pause_mouse_position = pygame.mouse.get_pos()

    pause_height = 640
    pause_width = 360

    pygame.draw.rect(SCREEN, 'black', [0, 100, pause_width, pause_height])
    pause_text = get_font(15).render("GAME PAUSED: TO Return PRESS ''ESC'' or ''P''", True, 'yellow')
    pause_rect = pause_text.get_rect(center=(640, 50))
    SCREEN.blit(pause_text, pause_rect)

    save_button_rect = pygame.Rect(30, 130, pause_width - 30, 50)
    main_menu_button_rect = pygame.Rect(30, 230, pause_width - 30, 50)
    close_game_button_rect = pygame.Rect(30, 330, pause_width - 30, 50)
    help_button_rect = pygame.Rect(30, 430, pause_width - 30, 50)

    # Change color based on mouse position
    save_color = 'red' if save_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    main_menu_color = 'red' if main_menu_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    close_game_color = 'red' if close_game_button_rect.collidepoint(pause_mouse_position) else 'yellow'
    help_color = 'red' if help_button_rect.collidepoint(pause_mouse_position) else 'yellow'

    # Draw buttons
    save_button_text = get_font(15).render('Save', True, save_color)
    main_menu_button_text = get_font(15).render('Main Menu', True, main_menu_color)
    close_game_button_text = get_font(15).render('Close Game', True, close_game_color)
    help_button_text = get_font(15).render('Help', True, help_color)

    SCREEN.blit(save_button_text, (30, 130))
    SCREEN.blit(main_menu_button_text, (30, 230))
    SCREEN.blit(close_game_button_text, (30, 330))
    SCREEN.blit(help_button_text, (30, 430))

    pygame.display.update()

    return save_button_rect, main_menu_button_rect, close_game_button_rect, help_button_rect


def draw_help() -> None:
    """
    This method draws the help menu on the screen.
    """
    global SCREEN
    pygame.init()  # Initialize Pygame
    help_height = 680
    help_width = 680
    help_surface = pygame.Surface((help_width, help_height))
    help_surface.fill('black')
    __GAME.get_inventory()
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
        3.potions:
            a.HEalth potion: use 'h'
            b.Vision potion: use 'v'\n\n
        
        good luck adventurer!!""")

    help_font = pygame.font.SysFont(None, 20)
    y_offset = 30
    for line in text.split('\n'):
        help_text = get_font(10).render(line, True, 'white')
        text_rect = help_text.get_rect(center=(233, y_offset))
        help_surface.blit(help_text, text_rect)
        y_offset += text_rect.height + 1

    SCREEN.blit(help_surface, (360, 70))

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


def get_message(message) -> None:
    """This function displays a message to the user based on actions in the dungeon."""
    message = get_font(24).render(message, True, 'white')
    message_rect = message.get_rect(center=(SCREEN.get_width() // 2, 610))
    SCREEN.blit(message, message_rect)
    pygame.display.flip()
    pygame.time.delay(100)
    pygame.display.flip()


def __gameplay(game: DungeonAdventure) -> None:
    """
    This method starts the gameplay for the Dungeon Adventure game and draws the game on the screen.
    Also handles the events for the game.
    :param game: The game object
    """
    global __GAME, pause, save, main_menu_button, close_game, help_option
    global SCREEN
    count = 0
    __GAME = game
    health_text = pygame.font.Font("Assets/Dungeon Depths.ttf", 12).render("Health", True, (255, 255, 255))
    title_text_rect = health_text.get_rect(center=(SCREEN.get_width() // 2, health_text.get_height() + 685))
    tile_size = MAX_TILE_SIZE - (REDUCTION_FACTOR_PER_DIFFICULTY * (DIFFICULTY))
    dungeon_width = tile_size * game.get_dungeon().get_dimensions()[0]
    dungeon_height = tile_size * game.get_dungeon().get_dimensions()[1]
    dungeon_starting_x = (SCREEN.get_width() - dungeon_width) // 2
    dungeon_starting_y = (SCREEN.get_height() - dungeon_height) // 2  #+ tile_size
    SCREEN.fill("black")
    draw_inventory(game.get_inventory())
    draw_dungeon(SCREEN, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                 dungeon_starting_y // tile_size)

    healthbar_width = SCREEN.get_width() // 3
    healthbar_height = 48
    healthbar_starting_x = dungeon_starting_x + (dungeon_width // 2) - (healthbar_width // 2) - 33
    healthbar_starting_y = health_text.get_height() + 625
    healthbar = Healthbar(game.get_player())
    SCREEN.blit(health_text, title_text_rect)
    music('Assets/Sounds/dungeon.wav', -1)
    while True:

        if not pause:
            pygame.display.set_caption('DUNGEON ADVENTURE')
            healthbar.draw(SCREEN, (healthbar_starting_x, healthbar_starting_y), (healthbar_width, healthbar_height))
        if pause:
            pygame.display.set_caption('PAUSE')
            save, main_menu_button, close_game, help_option = draw_pause()
            pygame.mixer.music.set_volume(0.5)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and pause:
                if save.collidepoint(event.pos):
                    save_game_state(__GAME)
                if main_menu_button.collidepoint(event.pos):
                    pause = False
                    music('Assets/Sounds/main_menu.wav',-1)
                    return
                if close_game.collidepoint(event.pos):
                    sys.exit()
                if help_option.collidepoint(event.pos):
                    draw_help()
            if event.type == pygame.KEYDOWN:
                if not pause:
                    if event.key == pygame.K_w:
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_MOVE_NORTH)
                        sound_efx('Assets/Sounds/footstep.wav',0)
                    elif event.key == pygame.K_s:
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_MOVE_SOUTH)
                        sound_efx('Assets/Sounds/footstep.wav',0)
                    elif event.key == pygame.K_a:
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_MOVE_WEST)
                        sound_efx('Assets/Sounds/footstep.wav',0)
                    elif event.key == pygame.K_d:
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_MOVE_EAST)
                        sound_efx('Assets/Sounds/footstep.wav',0)
                    elif event.key == pygame.K_h:
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_USE_HEALING_POTION)
                    elif event.key == pygame.K_v:
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_USE_VISION_POTION)
                    elif event.key == pygame.K_RETURN and can_exit():
                        __GAME.handle_event(DungeonEvent.GAMEPLAY_GOD_MODE)
                        display_win(SCREEN)
                        return
                else:
                    handle_cheat_code(event)
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause = not pause
                if game.get_battle_state():
                    Battle.start(SCREEN, game)
                    if not game.get_player().is_alive():
                        music('Assets/Sounds/defeat.wav', 0)
                        GameOver.start(SCREEN)
                        return
                SCREEN.fill("black")
                SCREEN.blit(health_text, title_text_rect)
                draw_inventory(game.get_inventory())
                draw_dungeon(SCREEN, game.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                             dungeon_starting_y // tile_size)
                healthbar.draw(SCREEN, (healthbar_starting_x, healthbar_starting_y),
                               (healthbar_width, healthbar_height))
            if __GAME.get_current_room() == __GAME.get_dungeon().get_exit():
                if not can_exit():
                    get_message("You must collect all 4 pillars of OOP to exit!")
                else:
                    get_message("Press Enter to escape!")
            # Handle custom events thrown by the game
            if event.type == pygame.USEREVENT:
                # If you fall into a pit, flash the screen and update the health bar
                if event.key == DungeonEvent.GAMEPLAY_PIT_DAMAGE:
                    flash_screen((255, 0, 0, 128))
                    sound_efx('Assets/Sounds/pit.wav', 0)
                    get_message("You have fallen into a pit!")
                    if not game.get_player().is_alive():
                        music('Assets/Sounds/defeat.wav', 0)
                        GameOver.start(SCREEN)
                        return
                if event.key == DungeonEvent.GAMEPLAY_USE_HEALING_POTION:
                    sound_efx('Assets/Sounds/heal.wav', 0)
                    flash_screen((0, 255, 0, 128))
                    get_message("You have use a heal potion!")
                if event.key == DungeonEvent.GAMEPLAY_USE_VISION_POTION:
                    sound_efx('Assets/Sounds/vision.wav', 0)
                    flash_screen((0, 0, 255, 128))
                    get_message("You have used a vision potion!")

        pygame.display.flip()
        pygame.time.delay(1000 // 60)


def display_win(screen: pygame.Surface) -> None:
    """
    This function displays the winning window for the user.
    :param screen: The screen that will be used for displaying.
    :return:
    """
    screen.fill("grey")
    # font = get_font
    music('Assets/Sounds/win.wav', 0)
    tile_size = MAX_TILE_SIZE - (REDUCTION_FACTOR_PER_DIFFICULTY * (DIFFICULTY))
    dungeon_width = tile_size * __GAME.get_dungeon().get_dimensions()[0]
    dungeon_height = tile_size * __GAME.get_dungeon().get_dimensions()[1]
    dungeon_starting_x = (SCREEN.get_width() - dungeon_width) // 2
    dungeon_starting_y = (SCREEN.get_height() - dungeon_height) // 2  # + tile_size
    draw_dungeon(SCREEN, __GAME.get_dungeon(), tile_size, dungeon_starting_x // tile_size,
                 dungeon_starting_y // tile_size)

    text = get_font(20).render("CONGRATS! YOU HAVE SUCCESSFULLY EXITED THE DUNGEON!", True, "black")
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, text.get_height()))
    main_menu_button = Button(image=None, position=(screen.get_width() // 2, screen.get_height() - 50),
                              text_input='Main Menu', font=get_font(20),
                              color_1="red", color_2="black")
    while True:
        main_menu_button.update(screen)
        for event in pygame.event.get():
            main_menu_button.change_color(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_input(event.pos):
                    pygame.mixer.music.stop()
                    music('Assets/Sounds/main_menu.wav', -1)
                    return
        pygame.display.update()

def flash_screen(color: tuple[int, int, int, int] = (0, 0, 0, 128)) -> None:
    """
    This method flashes the screen red.
    """
    prev_screen = SCREEN.copy()
    red_translucent = prev_screen.copy()
    red_translucent.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
    for _ in range(3):
        SCREEN.blit(red_translucent, (0, 0))
        pygame.display.flip()
        pygame.time.delay(50)
        SCREEN.blit(prev_screen, (0, 0))
        pygame.display.flip()
        pygame.time.delay(50)


def handle_cheat_code(event) -> None:
    """
    This method handles cheat code input for the game.
    :param event: The event to handle
    """
    global LAST_FOUR_BUTTONS
    if event.key == pygame.K_RETURN:
        if LAST_FOUR_BUTTONS == [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
            __GAME.handle_event(DungeonEvent.GAMEPLAY_GOD_MODE)
            LAST_FOUR_BUTTONS = []
    else:
        LAST_FOUR_BUTTONS.append(event.key)
        if len(LAST_FOUR_BUTTONS) > 4:
            LAST_FOUR_BUTTONS.pop(0)


def can_exit() -> bool:
    """
    This function checks whether the user has met requirements to exit the dungeon.
    :return: a boolean indicating whether the conditions have been met.
    """
    if (RoomItem.PillarOfInheritance.value in __GAME.get_inventory() and
            RoomItem.PillarOfAbstraction.value in __GAME.get_inventory() and
            RoomItem.PillarOfEncapsulation.value in __GAME.get_inventory() and
            RoomItem.PillarOfPolymorphism.value in __GAME.get_inventory() and
            __GAME.get_current_room() == __GAME.get_dungeon().get_exit()):
        return True
    return False


def draw_inventory(inventory: list[RoomItem]) -> None:
    """
    This method draws the inventory on the screen.
    :param inventory: The inventory to draw
    """
    inventory_text = get_font(15).render("Inventory", True, 'yellow')
    SCREEN.blit(inventory_text, (SCREEN.get_width() - inventory_text.get_width() - 10, 10))
    icon_size = 32

    x = SCREEN.get_width() - (icon_size + 20)
    y = 20 + inventory_text.get_height()

    count_items = defaultdict(int)
    for item in inventory:
        count_items[item] += 1
    image_to_count = {
        Tile.get_tile(Tile.INVENTORY_PILLAR_A, icon_size, icon_size): count_items[RoomItem.PillarOfAbstraction.value],
        Tile.get_tile(Tile.INVENTORY_PILLAR_E, icon_size, icon_size): count_items[RoomItem.PillarOfEncapsulation.value],
        Tile.get_tile(Tile.INVENTORY_PILLAR_I, icon_size, icon_size): count_items[RoomItem.PillarOfInheritance.value],
        Tile.get_tile(Tile.INVENTORY_PILLAR_P, icon_size, icon_size): count_items[RoomItem.PillarOfPolymorphism.value],
        Tile.get_tile(Tile.INVENTORY_HEALING_POTION, icon_size, icon_size): count_items[RoomItem.HealingPotion.value],
        Tile.get_tile(Tile.INVENTORY_VISION_POTION, icon_size, icon_size): count_items[RoomItem.VisionPotion.value],
    }
    pillars = 3
    for item_image, item_count in image_to_count.items():
        SCREEN.blit(item_image, (x, y))
        count_text = get_font(15).render(str(item_count), True, 'yellow')
        SCREEN.blit(count_text, (x - icon_size, y))
        y += icon_size
        if pillars <= 0:
            y += 10
        pillars -= 1


def draw_dungeon(screen: pygame.Surface, dungeon, room_size, x, y) -> None:
    """
    This method draws the dungeon on the screen.
    :param screen: The screen to draw the dungeon
    :param dungeon: The dungeon object
    :param room_size: The size of the room
    :param x: The starting x-coordinate
    :param y: The starting y-coordinate
    """
    root = dungeon.get_root()
    draw_room(screen, root, x, y, room_size, set())


def draw_room(screen: pygame.Surface, room: DungeonRoom, x, y, room_size, visited) -> None:
    """
    Recursively draw the room and its children on the screen.
    :param screen: The screen to draw the room
    :param room: The room to draw
    :param x: The x-coordinate of the room
    :param y: The y-coordinate of the room
    :param room_size: The size of the room
    :param visited: The set of visited rooms when drawing
    """
    if room is None or room in visited:
        return
    visited.add(room)
    if room not in __GAME.get_visited_rooms():
        for dx, dy, direction in [(1, 0, room.get_east()), (0, 1, room.get_south()), (-1, 0, room.get_west()),
                                  (0, -1, room.get_north())]:
            if direction:
                draw_room(screen, direction, x + dx, y + dy, room_size, visited)
        return
    mini_tile_size = room_size // 3
    for i in range(3):
        for j in range(3):
            tile = __get_appropriate_tile(room, j, i, mini_tile_size)
            screen.blit(tile, (x * room_size + i * mini_tile_size, y * room_size + j * mini_tile_size))
    for dx, dy, direction in [(1, 0, room.get_east()), (0, 1, room.get_south()), (-1, 0, room.get_west()),
                              (0, -1, room.get_north())]:
        if direction:
            draw_room(screen, direction, x + dx, y + dy, room_size, visited)


def __get_appropriate_tile(room: DungeonRoom, row, col, size) -> pygame.Surface:
    """
    This method returns the appropriate tile for the room based on the row and column of the room.
    :param room: The room to get the tile for
    :param row: The row of the room (0-2)
    :param col: The column of the room (0-2)
    :param size: The size of the tile
    :return: The tile for the room
    """
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
    elif len(room.get_items()) > 1 or room.get_monster() and len(room.get_items()) == 1:
        return Tile.get_tile(Tile.MULTIPLE_ITEMS, size, size)
    elif room.get_monster():
        monster_name = room.get_monster().get_name()
        return Tile.get_tile(Tile.MONSTER[monster_name], size, size)
    elif len(room.get_items()) == 1 and room.get_items()[0].value != RoomItem.Entrance.value:
        item = room.get_items()[0].value
        if item == RoomItem.PillarOfAbstraction.value:
            return Tile.get_tile(Tile.PILLAR_A, size, size)
        elif item == RoomItem.PillarOfEncapsulation.value:
            return Tile.get_tile(Tile.PILLAR_E, size, size)
        elif item == RoomItem.PillarOfInheritance.value:
            return Tile.get_tile(Tile.PILLAR_I, size, size)
        elif item == RoomItem.PillarOfPolymorphism.value:
            return Tile.get_tile(Tile.PILLAR_P, size, size)
        elif item == RoomItem.HealingPotion.value:
            return Tile.get_tile(Tile.HEALING_POTION, size, size)
        elif item == RoomItem.VisionPotion.value:
            return Tile.get_tile(Tile.VISION_POTION, size, size)
        elif item == RoomItem.Pit.value:
            return Tile.get_tile(Tile.PIT, size, size)
        else:
            raise ValueError(f"Invalid item attempting to be drawn: {item}")
    else:
        return Tile.get_tile(Tile.FLOOR, size, size)
