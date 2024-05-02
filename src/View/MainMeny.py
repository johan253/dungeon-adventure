from tkinter import Menu

import pygame
from pygame.locals import *


class MainMenu:
    def __init__(self):
        pygame.init()
        self.hero_select_visible = False
        self.load_game_visible = False
        self.font = pygame.font.SysFont('Arial', 32)
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption('Main Menu')
        pygame.mouse.set_visible(True)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            self.screen.fill((0, 0, 0))
            self.screen.blit(pygame.image.load("Assets/mainmenu.jpg"), (0, 0))

            cursor = pygame.mouse.get_pos()
            if self.hero_select_visible:
                self.hero_select_visible = True
            elif self.load_game_visible:
                self.load_game_visible = True
            else:
                play_button = pygame.Rect(100, 200, 100, 50)
                load_button = pygame.Rect(100, 200, 100, 50)
                quit_button = pygame.Rect(100, 200, 100, 50)
                about_button = pygame.Rect(100, 200, 100, 50)


                pygame

