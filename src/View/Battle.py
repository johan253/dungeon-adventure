import pygame
import sys
from src.controller.DungeonAdventure import DungeonAdventure

# Define custom events
SPECIAL_ATTACK = pygame.USEREVENT + 1
CUSTOM_USE_ITEM = pygame.USEREVENT + 3


def start(screen, game: DungeonAdventure):
    """
    This method starts the battle sequence for the Dungeon Adventure game.
    :param screen: The screen to draw the battle
    :param game: The game object
    """
    screen.fill((122, 255, 255))
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Attack button (example: 'A' key)
                    pygame.event.post(pygame.event.Event(SPECIAL_ATTACK))
                elif event.key == pygame.K_i:  # Use item button (example: 'I' key)
                    item_event = pygame.event.Event(CUSTOM_USE_ITEM, item_type='RoomItem')
                    pygame.event.post(item_event)
            game.process_event(event)

        pygame.display.update()
        pygame.time.delay(1000 // 60)  # Limit the loop to 60 frames per second

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set the screen size
    pygame.display.set_caption("Dungeon Adventure Battle")

    # Initialize the game with player name and class, replace with data from db if needed
    dungeon_adv = DungeonAdventure('PlayerName', "Warrior")

    start(screen, dungeon_adv)
