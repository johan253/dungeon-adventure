import pygame
from View.MainMenu import get_font
from View.MainMenu import main_menu
from View.Button import Button


def start(screen: pygame.Surface) -> None:
    """
    This method starts the game over sequence for the Dungeon Adventure game.
    :param screen: The screen to draw the game over
    """
    screen.fill("black")
    # font = get_font
    text = get_font(45).render("Game Over", True, "red")
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2
                       - text.get_height() // 2))

    main_menu_button = Button(image=None, position=(screen.get_width() // 2, screen.get_height() // 2 + 250),
                              text_input='Main Menu', font=get_font(20),
                              color_1="red", color_2="white")
    while True:
        main_menu_button.update(screen)
        for event in pygame.event.get():
            main_menu_button.change_color(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_input(event.pos):
                    main_menu()
        pygame.display.update()


def ending(screen: pygame.Surface) -> None:
    screen.fill("grey")
    # font = get_font
    text = get_font(20).render("CONGRATS! YOU HAVE SUCCESSFULLY EXITED THE DUNGEON!", True, "black")
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2
                   - text.get_height() // 2))

    main_menu_button = Button(image=None, position=(screen.get_width() // 2, screen.get_height() // 2 + 250),
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
                    main_menu()
        pygame.display.update()
