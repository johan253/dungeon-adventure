import pygame
import sys
from Button import Button
from SaveLoadManager import SaveLoadSystem
from View.TextField import TextField
from src.controller.DungeonAdventure import DungeonAdventure
from src.model.Priestess import Priestess
from src.model.Thief import Thief
from src.model.Warrior import Warrior

pygame.init()

Screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Main Menu')

background = pygame.image.load('Assets/mainmenu.png')
background = pygame.transform.scale(background, (1280, 720))

saveManager = SaveLoadSystem(".save", "save_data")

game: DungeonAdventure | None = None


def get_font(size):
    return pygame.font.Font('Assets/Dungeon Depths.ttf', size)

def play():
    while True:
        play_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        play_text = get_font(15).render('START A NEW GAME:', True, (0, 255, 0))
        play_rect = play_text.get_rect(center=(640, 160))
        Screen.blit(play_text, play_rect)

        play_new_game_button = Button(image=None, position=(640, 360), text_input='NEW GAME', font=get_font(15),
                                      color_1="white", color_2="red")

        play_back_button = Button(image=None, position=(640, 560), text_input='BACK', font=get_font(15),
                                  color_1="white", color_2="red")

        play_back_button.change_color([play_mouse_position[0], play_mouse_position[1]])
        play_new_game_button.change_color([play_mouse_position[0], play_mouse_position[1]])
        play_back_button.update(Screen)
        play_new_game_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_back_button.check_input(play_mouse_position):
                    main_menu()
                if play_new_game_button.check_input(play_mouse_position):
                    select_name()
        pygame.display.update()


def select_name():
    text_field = TextField(440, 360, 400, 50)
    name = ""
    Screen.fill("black")
    while True:
        name = text_field.get_text()
        continue_button = Button(image=None, position=(640, 460), text_input='CONTINUE', font=get_font(15),
                                 color_1="white", color_2="red")
        back_button = Button(image=None, position=(640, 560), text_input='BACK', font=get_font(15),
                             color_1="white", color_2="red")
        continue_button.change_color([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
        continue_button.update(Screen)
        back_button.change_color([pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]])
        back_button.update(Screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            text_field.handle_event(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.check_input(pygame.mouse.get_pos()):
                    play()
                if continue_button.check_input(pygame.mouse.get_pos()):
                    if name.strip() != "":
                        select_hero(name.strip())

        text_field.draw(Screen)
        pygame.display.update()


def select_hero(player_name: str):
    while True:
        play_mouse_position = pygame.mouse.get_pos()

        Screen.fill("dark blue")

        play_text = get_font(15).render(f'WELCOME {player_name} THE BRAVE! SELECT A HERO:', True, (255,255,255))
        play_rect = play_text.get_rect(center=(640, 100))
        Screen.blit(play_text, play_rect)

        play_thief_button = Button(image=None, position=(640, 260), text_input='THIEF', font=get_font(15),
                                   color_1="white", color_2="red")

        play_warrior_button = Button(image=None, position=(640, 360), text_input='WARRIOR', font=get_font(15),
                                     color_1="white", color_2="red")

        play_priestess_button = Button(image=None, position=(640, 460), text_input='PRIESTESS', font=get_font(15),
                                       color_1="white", color_2="red")

        play_back_button = Button(image=None, position=(640, 660), text_input='BACK', font=get_font(15),
                                  color_1="white", color_2="red")

        play_back_button.change_color([play_mouse_position[0], play_mouse_position[1]])
        play_thief_button.change_color([play_mouse_position[0], play_mouse_position[1]])
        play_warrior_button.change_color([play_mouse_position[0], play_mouse_position[1]])
        play_priestess_button.change_color([play_mouse_position[0], play_mouse_position[1]])

        play_back_button.update(Screen)
        play_thief_button.update(Screen)
        play_warrior_button.update(Screen)
        play_priestess_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                global game
                if play_back_button.check_input(play_mouse_position):
                    gameplay()
                if play_thief_button.check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, Thief)
                    saveManager.save_data(game.get_state(), "current_state")
                    gameplay()
                if play_warrior_button.check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, Warrior)
                    saveManager.save_data(game.get_state(), "current_state")
                    gameplay()
                if play_priestess_button.check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, Priestess)
                    saveManager.save_data(game.get_state(), "current_state")
                    gameplay()
        pygame.display.update()


def gameplay():
    print(game.get_state())
    while True:
        play_mouse_position = pygame.mouse.get_pos()

        Screen.fill("gray")

        # play_text = get_font(15).render('Gameplay', True, (0, 255, 0))
        # play_rect = play_text.get_rect(center=(640, 260))
        # Screen.blit(play_text, play_rect)
        #
        # play_back_button = Button(image=None, position=(640, 460), text_input='Back', font=get_font(15),
        #                           color_1="white", color_2="grey")
        #
        # play_back_button.change_color([play_back_button.x_position, play_back_button.y_position])
        # play_back_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # saveLoadManager()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: Add gameplay logic
                continue
        pygame.display.update()


def load():
    while True:
        load_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        load_text = get_font(15).render('MAKE A SELECTION:', True, (0, 255, 0))
        load_rect = load_text.get_rect(center=(640, 160))
        Screen.blit(load_text, load_rect)

        load_back_button = Button(image=None, position=(640, 460), text_input='BACK', font=get_font(15),
                                  color_1="white", color_2="red")
        load_button = Button(image=None, position=(640, 306), text_input='LOAD SAVED GAME', font=get_font(15),
                             color_1="white", color_2="red")

        load_back_button.change_color([load_mouse_position[0], load_mouse_position[1]])
        load_button.change_color([load_mouse_position[0], load_mouse_position[1]])
        load_button.update(Screen)
        load_back_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_back_button.check_input(load_mouse_position):
                    main_menu()
                if load_button.check_input(load_mouse_position):
                    main_menu()
                if load_button.check_input(load_mouse_position):
                    gameplay()
        pygame.display.update()


def about():
    info = """Welcome to Dungeon Adventure!
    
    Dungeon Adventure v1.0
    
    This game was created by Aly Badr, Johan Hernandez, Lwazi Mabota.
    
    In this game a user will have the option to select from three classes \b(Thief, Warrior, Wizard) with which they
    will explore the dungeon and attempt to escape. The user will have to find the four pillars of OOP before they
    can escape. While trying to find these pillars they will encounter a few things that could either progress the
    game or halt the game should their health fall to 0. The user can encounter monsters and pits which will take
    away from their health, but they can also find potions that will restore their health or expose parts of the
    dungeon that they have yet to explore.
    
    Good luck!"""

    while True:
        about_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        lines = info.split('\n')  # Split the text into lines
        y_offset = 100  # Initial Y offset for the first line

        for line in lines:
            about_text = get_font(10).render(line, True, (255, 255, 255))  # Render each line separately
            about_rect = about_text.get_rect(center=(640, y_offset))
            Screen.blit(about_text, about_rect)
            y_offset += about_rect.height + 10  # Update Y offset for the next line

        about_back = Button(image=None, position=(655, 660), text_input='BACK', font=get_font(15),
                            color_1="white", color_2="red")

        about_back.change_color(about_mouse_position)
        about_back.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if about_back.check_input(about_mouse_position):
                    main_menu()

        pygame.display.update()


def main_menu():
    while True:
        Screen.blit(background, (0, 0))

        mouse_position = pygame.mouse.get_pos()

        menu_text = get_font(50).render("DUNGEON ADVENTURE", True, "White")
        menu_rect = menu_text.get_rect(center=(650, 100))

        play_button = Button(image=pygame.image.load('Assets/play.png'), position=(650, 260), text_input="PLAY",
                             font=get_font(30), color_1="White", color_2="White")
        load_button = Button(image=pygame.image.load('Assets/load.png'), position=(650, 460), text_input="LOAD",
                             font=get_font(30), color_1="White", color_2="White")
        about_button = Button(image=pygame.image.load('Assets/about.png'), position=(650, 630), text_input="ABOUT",
                              font=get_font(30), color_1="White", color_2="White")

        Screen.blit(menu_text, menu_rect)

        for button in (play_button, load_button, about_button):
            button.change_color(mouse_position)
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_input(mouse_position):
                    play()
                if load_button.check_input(mouse_position):
                    load()
                if about_button.check_input(mouse_position):
                    about()
        pygame.display.update()


main_menu()
