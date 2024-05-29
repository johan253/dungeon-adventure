import pygame
from src.View.Button import Button

def start(screen: pygame.Surface) -> None:
    """
    This method starts the game over sequence for the Dungeon Adventure game.
    :param screen: The screen to draw the game over
    """
    screen.fill("black")
    font = pygame.font.Font(None, 100)
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - text.get_height() // 2))
    main_menu_button = Button(image=None, position=(screen.get_width() // 2, screen.get_height() // 2 + 250),
                              text_input='Main Menu', font=pygame.font.Font(None, 32),
                              color_1="white", color_2="red")
    while True:
        main_menu_button.update(screen)
        for event in pygame.event.get():
            main_menu_button.change_color(pygame.mouse.get_pos())
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if main_menu_button.check_input(event.pos):
                    return
        pygame.display.update()
