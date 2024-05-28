import pygame
import sys
from src.controller.DungeonAdventure import DungeonAdventure
from src.model.DungeonCharacter import DungeonCharacter
from View.Healthbar import Healthbar
from View.MainMenu import get_font

ENEMY = None
SCREEN: pygame.Surface | None = None
GAME: DungeonAdventure | None = None


def start(the_screen: pygame.Surface, game: DungeonAdventure):
    """
    This method starts the battle sequence for the Dungeon Adventure game.
    :param the_screen: The screen to draw the battle
    :param game: The game object
    """
    global ENEMY, SCREEN, GAME
    the_screen.fill((122, 255, 255))
    running = True
    SCREEN = the_screen
    GAME = game
    ENEMY = game.get_current_room().get_monster()
    if ENEMY is None:
        raise Exception("No enemy in room")
    __draw_battle_scene(game.get_player(), ENEMY)


def __draw_battle_scene(player: DungeonCharacter, enemy: DungeonCharacter):
    """
    This method draws the battle scene on the screen.
    :param player: The player object
    :param enemy: The enemy object
    """
    SCREEN.fill((0, 0, 0))
    font = get_font(12)
    player_name = font.render(player.get_name(), True, (255, 255, 255))
    player_healthbar = Healthbar(player)
    player_speed = font.render(f"Speed: {player.get_attack_speed()}", True, (255, 255, 255))

    enemy_name = font.render(enemy.get_name(), True, (255, 255, 255))
    enemy_healthbar = Healthbar(enemy)
    enemy_speed = font.render(f"Speed: {enemy.get_attack_speed()}", True, (255, 255, 255))
    while True:

        SCREEN.blit(player_name, (50, 50))
        SCREEN.blit(player_speed, (50, 200))

        SCREEN.blit(enemy_name, (SCREEN.get_width() // 2 + 50, 50))
        SCREEN.blit(enemy_speed, (SCREEN.get_width() // 2 + 50, 200))
        player_healthbar.draw(SCREEN, (50, 100), (250, 20))
        enemy_healthbar.draw(SCREEN, (SCREEN.get_width() // 2 + 50, 100), (250, 20))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                GAME.handle_event(event)

        pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set the screen size
    pygame.display.set_caption("Dungeon Adventure Battle")

    # Initialize the game with player name and class, replace with data from db if needed
    dungeon_adv = DungeonAdventure('PlayerName', "Warrior")

    start(screen, dungeon_adv)
