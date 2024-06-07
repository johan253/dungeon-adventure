import pygame, sys
from View.Button import Button
from View import Gameplay
from View.TextField import TextField
from model.DugeonRoom import DungeonRoom
from src.controller.DungeonAdventure import DungeonAdventure
from src.model.CharacterFactory import CharacterFactory
from src.model.Dungeon import Dungeon

pygame.init()

Screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('DUNGEON ADVENTURE')

background = pygame.image.load('Assets/mainmenu.png')
background = pygame.transform.scale(background, (1280, 720))

thief_image = pygame.image.load('Assets/info_thief.png')
warrior_image = pygame.image.load('Assets/info_warrior.png')
priest_image = pygame.image.load('Assets/info_priestess.png')

game: DungeonAdventure | None = None


def get_font(size):
    return pygame.font.Font('Assets/Dungeon Depths.ttf', size)



def play():
    while True:
        pygame.display.set_caption('PLAY')

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
                    return
                if play_new_game_button.check_input(play_mouse_position):
                    select_name()
        pygame.display.update()


def select_name():
    text_field = TextField(440, 360, 400, 50)
    enter_name_text = get_font(15).render('Enter your name:', True, "white")
    enter_name_rect = enter_name_text.get_rect(center=(640, 260))
    continue_button = Button(image=None, position=(640, 560), text_input='Continue', font=get_font(15),
                             color_1="white", color_2="red")
    back_button = Button(image=None, position=(640, 660), text_input='Back', font=get_font(15),
                         color_1="white", color_2="red")
    name = ""
    while True:
        pygame.display.set_caption('SELECT NAME')
        Screen.fill("black")
        Screen.blit(enter_name_text, enter_name_rect)
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
                    return
                if continue_button.check_input(pygame.mouse.get_pos()):
                    if name.strip() != "":
                        select_hero(name.strip())
                        return

        text_field.draw(Screen)
        pygame.display.update()


def select_hero(player_name: str):
    buttons: dict[str, Button] = {
        "thief": Button(image=None, position=(620, 100), text_input='Thief', font=get_font(15),
                        color_1="white", color_2='orange'),

        "warrior": Button(image=None, position=(640, 300), text_input='Warrior', font=get_font(15),
                          color_1="white", color_2="red"),

        "priestess": Button(image=None, position=(645, 500), text_input='Priestess', font=get_font(15),
                            color_1="white", color_2="purple"),

        "back": Button(image=None, position=(620, 700), text_input='Back', font=get_font(15),
                       color_1="white", color_2="red")
    }
    play_text = get_font(15).render(f'Welcome {player_name}! Select a Hero:', True, 'cyan')
    play_rect = play_text.get_rect(center=(640, 40))

    while True:
        pygame.display.set_caption('SELECT HERO')
        play_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")
        Screen.blit(thief_image, (440, 138))
        Screen.blit(warrior_image, (440, 338))
        Screen.blit(priest_image, (440, 538))
        Screen.blit(play_text, play_rect)

        warrior_stats = ("""health: 125
        \nmin/max damage: 35/60                       
        \nattack speed: 4
        \nchance to hit: 0.8
        \nchance to block: 0.2
                         """)
        warrior_lines = warrior_stats.split('\n')  # Split the text into lines
        warrior_y_offset = 340  # Initial Y offset for the first line
        for warrior_stat in warrior_lines:
            warrior_text = get_font(8).render(warrior_stat, True, 'yellow')
            warrior_rect = warrior_text.get_rect(midleft=(580, warrior_y_offset))
            Screen.blit(warrior_text, warrior_rect)
            warrior_y_offset += warrior_rect.height + 0.5

        thief_stats = ("""health: 75
        \nmin/max damage: 20/40                       
        \nattack speed: 6
        \nchance to hit: 0.8
        \nchance to block: 0.4
                         """)
        thief_lines = thief_stats.split('\n')  # Split the text into lines
        thief_y_offset = 140  # Initial Y offset for the first line
        for thief_stat in thief_lines:
            thief_text = get_font(8).render(thief_stat, True, 'yellow')
            thief_rect = thief_text.get_rect(midleft=(580, thief_y_offset))
            Screen.blit(thief_text, thief_rect)
            thief_y_offset += thief_rect.height + 0.5

        priestess_stats = ("""health: 75
        \nmin/max damage: 25/45                       
        \nattack speed: 5
        \nchance to hit: 0.7
        \nchance to block: 0.3
                         """)
        priestess_lines = priestess_stats.split('\n')  # Split the text into lines
        priestess_y_offset = 540  # Initial Y offset for the first line
        for priestess_stat in priestess_lines:
            priestess_text = get_font(8).render(priestess_stat, True, 'yellow')
            priestess_rect = priestess_text.get_rect(midleft=(580, priestess_y_offset))
            Screen.blit(priestess_text, priestess_rect)
            priestess_y_offset += priestess_rect.height + 0.5

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
                    return
                if buttons["thief"].check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, CharacterFactory.THIEF)
                    Gameplay.play(Screen, game)
                    return
                if buttons["warrior"].check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, CharacterFactory.WARRIOR)
                    Gameplay.play(Screen, game)
                    return
                if buttons["priestess"].check_input(play_mouse_position):
                    game = DungeonAdventure(player_name, CharacterFactory.PRIESTESS)
                    Gameplay.play(Screen, game)
                    return
        pygame.display.update()


def load():
    while True:
        pygame.display.set_caption('LOAD')

        load_mouse_position = pygame.mouse.get_pos()

        Screen.fill("black")

        load_text = get_font(24).render('Select Load to Continue a Previous game:', True, (255, 255, 0))
        load_rect = load_text.get_rect(center=(650, 60))
        Screen.blit(load_text, load_rect)

        load_button = Button(image=None, position=(640, 360), text_input='LOAD GAME', font=get_font(24),
                             color_1="white", color_2="red")
        load_back_button = Button(image=None, position=(640, 610), text_input='Back', font=get_font(24),
                                  color_1="white", color_2="red")
        load_back_button.change_color([load_mouse_position[0], load_mouse_position[1]])
        load_back_button.update(Screen)
        load_button.change_color([load_mouse_position[0], load_mouse_position[1]])
        load_button.update(Screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if load_back_button.check_input(load_mouse_position):
                    return
                if load_button.check_input(load_mouse_position):
                    game_state = Gameplay.load_game_state()
                    if game_state:
                        Gameplay.play(Screen, game_state)
                        return

        pygame.display.update()


def about():
    pygame.display.set_caption('ABOUT')

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
                    return

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
        pygame.display.set_caption('MAIN MENU')
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
