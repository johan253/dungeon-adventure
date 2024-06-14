import os, pygame
os.chdir(__file__[:-8] + "/View")
pygame.init()
import View.MainMenu as MainMenu

MainMenu.main_menu()