import pygame, sys
from Button import Button
from View import Gameplay
from View.TextField import TextField
from model.DugeonRoom import DungeonRoom
from src.controller.DungeonAdventure import DungeonAdventure
from SaveLoadManager import SaveLoadSystem
from src.model.CharacterFactory import CharacterFactory
from src import SaveLoadManager
from src.model.Dungeon import Dungeon

pygame.init()

Screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Main Menu')

background = pygame.image.load('Assets/mainmenu.png')
background = pygame.transform.scale(background, (1280, 720))

game: DungeonAdventure | None = None
save_data = SaveLoadSystem(".save", "saved_data")
# game_data = save_data.load_data("save_data")




def get_font(size):
    return pygame.font.Font('Assets/Dungeon Depths.ttf', size)


def play():
    while True:
        play_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        play_text = get_font(15).render('Play', True, (255, 255, 0))
        play_rect = play_text.get_rect(center=(640, 260))
        Screen.blit(play_text, play_rect)

        play_new_game_button = Button(image=None, position=(640, 360), text_input='New Game', font=get_font(15),
                                      color_1="white", color_2="red")

        play_back_button = Button(image=None, position=(640, 460), text_input='Back', font=get_font(15),
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
    continue_button = Button(image=None, position=(640, 460), text_input='Continue', font=get_font(15),
                             color_1="white", color_2="red")
    back_button = Button(image=None, position=(640, 560), text_input='Back', font=get_font(15),
                         color_1="white", color_2="red")
    name = ""
    while True:
        Screen.fill("black")
        name = text_field.get_text()

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
    buttons: dict[str, Button] = {
        "thief": Button(image=None, position=(640, 260), text_input='Thief', font=get_font(15),
                        color_1="white", color_2="red"),

        "warrior": Button(image=None, position=(640, 360), text_input='Warrior', font=get_font(15),
                          color_1="white", color_2="red"),

        "priestess": Button(image=None, position=(640, 460), text_input='Priestess', font=get_font(15),
                            color_1="white", color_2="red"),

        "back": Button(image=None, position=(640, 660), text_input='Back', font=get_font(15),
                       color_1="white", color_2="red")
    }
    play_text = get_font(15).render(f'Welcome {player_name}! Select a Hero:', True, (255, 255, 0))
    play_rect = play_text.get_rect(center=(640, 160))
    while True:
        play_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        Screen.blit(play_text, play_rect)

        for button in buttons.values():
            button.change_color([play_mouse_position[0], play_mouse_position[1]])
            button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                global game
                if buttons["back"].check_input(play_mouse_position):
                    play()
                if buttons["thief"].check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, CharacterFactory.THIEF)
                    Gameplay.play(game)
                if buttons["warrior"].check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, CharacterFactory.WARRIOR)
                    Gameplay.play(game)
                if buttons["priestess"].check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, CharacterFactory.PRIESTESS)
                    Gameplay.play(game)
        pygame.display.update()


def load():
    while True:
        load_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        load_text = get_font(15).render('Load', True, (0, 255, 0))
        load_rect = load_text.get_rect(center=(640, 260))
        Screen.blit(load_text, load_rect)

        load_back_button = Button(image=None, position=(640, 460), text_input='Back', font=get_font(15),
                                  color_1="white", color_2="red")
        load_back_button = Button(image=None, position=(640, 460), text_input='Back', font=get_font(15),
                                  color_1="white", color_2="red")
        load_back_button.change_color([load_mouse_position[0], load_mouse_position[1]])
        load_back_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_back_button.check_input(load_mouse_position):
                    save_data.save_data_from(game_data, "save_data")
        pygame.display.update()


def about():
    info = """Welcome to Dungeon Adventure!
    
    Dungeon Adventure v1.0
    
    This game was created by Aly Badr, Johan Hernandez, Lwazi Mabota.
    
    In this game a user will have the option to select from three classes(Thief, Warrior, Wizard) with which they
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
            about_text = get_font(10).render(line, True, (0, 255, 0))  # Render each line separately
            about_rect = about_text.get_rect(center=(640, y_offset))
            Screen.blit(about_text, about_rect)
            y_offset += about_rect.height + 10  # Update Y offset for the next line

        about_back = Button(image=None, position=(655, 660), text_input='Back', font=get_font(15),
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
    menu_text = get_font(50).render("Dungeon Adventure", True, "White")
    menu_rect = menu_text.get_rect(center=(650, 100))

    play_button = Button(image=pygame.image.load('Assets/play.png'), position=(650, 260), text_input="PLAY",
                         font=get_font(30), color_1="White", color_2="red")
    load_button = Button(image=pygame.image.load('Assets/load.png'), position=(650, 460), text_input="LOAD",
                         font=get_font(30), color_1="White", color_2="red")
    about_button = Button(image=pygame.image.load('Assets/about.png'), position=(650, 650), text_input="ABOUT",
                          font=get_font(30), color_1="White", color_2="red")
    while True:
        Screen.blit(background, (0, 0))

        mouse_position = pygame.mouse.get_pos()

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


if __name__ == '__main__':
    main_menu()
