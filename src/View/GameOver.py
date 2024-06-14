import pygame
from View.Button import Button


def start(screen: pygame.Surface) -> None:
    """
    This method starts the game over sequence for the Dungeon Adventure game.
    :param screen: The screen to draw the game over
    """
    screen.fill("black")
    # font = get_font
    text = pygame.font.Font(None, 45).render("Game Over", True, "red")
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2
                       - text.get_height() // 2))

    main_menu_button = Button(image=None, position=(screen.get_width() // 2, screen.get_height() // 2 + 250),
                              text_input='Main Menu', font=pygame.font.Font(None, 24),
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
                    return        pygame.display.update()


def ending(screen: pygame.Surface) -> None:
    """
    This function displays a new window should the user exit the game successfully.
    :param screen: The screen that the window will be on.
    :return:
    """
    screen.fill("grey")
    # font = get_font
    text = pygame.font.Font(None, 24).render("CONGRATS! YOU HAVE SUCCESSFULLY EXITED THE DUNGEON!", True, "black")
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2
                   - text.get_height() // 2))

    main_menu_button = Button(image=None, position=(screen.get_width() // 2, screen.get_height() // 2 + 250),
                              text_input='Main Menu', font=pygame.font.Font(None, 24),
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
                    return        pygame.display.update()
