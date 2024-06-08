import pygame
import sys
import src.controller.DungeonEvent as DungeonEvent
from View.PlaySound import music, sound_efx
from src.controller.DungeonAdventure import DungeonAdventure
from src.model.DungeonCharacter import DungeonCharacter
from src.model.RoomItem import RoomItem
from View.Healthbar import Healthbar
from View.MainMenu import get_font
from View import Sprite

FONT = get_font(12)
ENEMY: DungeonCharacter | None = None
SCREEN: pygame.Surface | None = None
GAME: DungeonAdventure | None = None
BATTLE_OPTIONS: list[str] = [
    "Normal Attack",
    "Special Attack",
    "Use Heal Potion:  "]
# The position of the battle options / dialogue box
OPTIONS_POS = (0, 0)
SELECTED_OPTION = 0

# Boolean to determine if a dialogue box is open
OPEN_DIALOGUE = False
# The text to display in the dialogue box
DIALOGUE = ""


def start(the_screen: pygame.Surface, game: DungeonAdventure) -> None:
    """
    This method starts the battle sequence for the Dungeon Adventure game.
    :param the_screen: The screen to draw the battle
    :param game: The game object
    """
    global ENEMY, SCREEN, GAME, OPTIONS_POS
    SCREEN = the_screen
    GAME = game
    ENEMY = game.get_current_room().get_monster()
    OPTIONS_POS = (50, SCREEN.get_height() - 200)
    update_available_health_potions()

    if ENEMY is None:
        raise Exception("No enemy in room")
    __draw_battle_scene(game.get_player(), ENEMY)


def __draw_battle_scene(player: DungeonCharacter, enemy: DungeonCharacter) -> None:
    """
    This method draws the battle scene on the screen.
    :param player: The player object
    :param enemy: The enemy object
    """
    SCREEN.fill((0, 0, 0))
    player_image = Sprite.get_sprite(player.DEFAULT_NAME)
    player_name = FONT.render(player.get_name(), True, (255, 255, 255))
    player_healthbar = Healthbar(player)
    player_speed = FONT.render(f"Speed: {player.get_attack_speed()}", True, (255, 255, 255))

    enemy_image = Sprite.get_sprite(enemy.DEFAULT_NAME)
    enemy_name = FONT.render(enemy.get_name(), True, (255, 255, 255))
    enemy_healthbar = Healthbar(enemy)
    enemy_speed = FONT.render(f"Speed: {enemy.get_attack_speed()}", True, (255, 255, 255))
    while True:
        SCREEN.fill("black")

        # Draw the player information and Sprite
        SCREEN.blit(player_name, (50, 50))
        SCREEN.blit(player_speed, (50, 150))
        SCREEN.blit(player_image, (50, 200))

        # Draw the enemy information and Sprite
        SCREEN.blit(enemy_name, (SCREEN.get_width() // 2 + 50, 50))
        SCREEN.blit(enemy_speed, (SCREEN.get_width() // 2 + 50, 150))
        SCREEN.blit(enemy_image, (SCREEN.get_width() // 2 + 50, 200))

        # Draw the health bars
        player_healthbar.draw(SCREEN, (50, 100), (250, 20))
        enemy_healthbar.draw(SCREEN, (SCREEN.get_width() // 2 + 50, 100), (250, 20))

        # Draw the battle options / dialog box
        draw_battle_options()
        # Draw the help text
        draw_help_text()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                handle_keydown(event)
                if not GAME.get_battle_state() and not OPEN_DIALOGUE:
                    return

        pygame.display.update()
        pygame.time.delay(1000//60)


def handle_keydown(event: pygame.event.Event) -> None:
    """
    This method handles the keydown event for the battle scene.
    :param event: The keydown event
    """
    global SELECTED_OPTION, OPEN_DIALOGUE, DIALOGUE
    the_action = None
    # Move the selected option up or down
    if event.key == pygame.K_DOWN:
        SELECTED_OPTION = (SELECTED_OPTION + 1) % len(BATTLE_OPTIONS)
    elif event.key == pygame.K_UP:
        SELECTED_OPTION = (SELECTED_OPTION - 1) % len(BATTLE_OPTIONS)
    # Confirm the selected option
    elif event.key == pygame.K_RETURN:
        # If a dialogue box is open, close it
        if OPEN_DIALOGUE:
            OPEN_DIALOGUE = False
            DIALOGUE = ""
            return
        # else, handle the selected option
        if SELECTED_OPTION == 0:
            the_action = DungeonEvent.BATTLE_ATTACK
            sound_efx('Assets/Sounds/attack.wav', 0)
        elif SELECTED_OPTION == 1:
            the_action = DungeonEvent.BATTLE_SPECIAL
            sound_efx('Assets/Sounds/attack.wav', 0)
        elif SELECTED_OPTION == 2:
            the_action = DungeonEvent.BATTLE_HEAL
            sound_efx('Assets/Sounds/heal.wav', 0)
    # If an action was selected, handle the action
    if the_action is None:
        return
    # Handle the action and update the dialogue box
    OPEN_DIALOGUE = True
    player_name = GAME.get_player().get_name()
    player_starting_health = GAME.get_player().get_health()
    enemy_name = ENEMY.get_name()
    enemy_starting_health = ENEMY.get_health()
    # Handle the action
    GAME.handle_event(the_action)
    # Update the dialogue box
    if the_action == DungeonEvent.BATTLE_ATTACK:
        DIALOGUE = (f"{player_name} and {enemy_name} exchange blows! \n"
                    f"{player_name} health: {player_starting_health} -> {GAME.get_player().get_health()} \n"
                    f"{enemy_name} health: {enemy_starting_health} -> {ENEMY.get_health()}\n")
    elif the_action == DungeonEvent.BATTLE_SPECIAL:
        DIALOGUE = (f"{player_name} uses a special attack and exchanges blows with {enemy_name}! \n"
                    f"{player_name} health: {player_starting_health} -> {GAME.get_player().get_health()} \n"
                    f"{enemy_name} health: {enemy_starting_health} -> {ENEMY.get_health()}\n")
    elif the_action == DungeonEvent.BATTLE_HEAL:
        DIALOGUE = f"{player_name} heals for {GAME.get_player().get_health() - player_starting_health} health"
        update_available_health_potions()


def draw_battle_options() -> None:
    """
    This method draws the battle options on the screen.
    """
    global OPEN_DIALOGUE, DIALOGUE
    # If a dialogue box is open, draw the dialogue box
    if OPEN_DIALOGUE:
        lines = DIALOGUE.split("\n")
        y_offset = 0
        for line in lines:
            text_surface = FONT.render(line, True, "white")
            SCREEN.blit(text_surface, (OPTIONS_POS[0], OPTIONS_POS[1] - 50 + y_offset))
            y_offset += FONT.get_height()
        return
    # else, draw the battle options menu
    for i, option in enumerate(BATTLE_OPTIONS):
        color = "white"
        # Highlight the selected option
        if i == SELECTED_OPTION:
            color = "red"
        text_surface = FONT.render(option, True, color)
        SCREEN.blit(text_surface, (OPTIONS_POS[0], OPTIONS_POS[1] + i * (FONT.get_height() + 10)))


def draw_help_text() -> None:
    """
    This method draws the help text on the screen.
    """
    text = FONT.render("Use the arrow keys to select an option and press enter to confirm", True, "white")
    # If a dialogue box is open, display the continue text
    if OPEN_DIALOGUE:
        text = FONT.render("Press enter to continue", True, "white")
    SCREEN.blit(text, (SCREEN.get_width() // 2 - text.get_width() // 2, SCREEN.get_height() - text.get_height() - 10))


def update_available_health_potions() -> None:
    """
    This method updates the number of available health potions.
    """
    # Update the number of available health potions replacing the last character of the string
    health_potion_option = list(BATTLE_OPTIONS[len(BATTLE_OPTIONS) - 1])
    health_potion_option[-1] = str(GAME.get_inventory().count(RoomItem.HealingPotion.value))
    BATTLE_OPTIONS[len(BATTLE_OPTIONS) - 1] = "".join(health_potion_option)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))  # Set the screen size
    pygame.display.set_caption("Dungeon Adventure Battle")

    # Initialize the game with player name and class, replace with data from db if needed
    dungeon_adv = DungeonAdventure('PlayerName', "Warrior")

    start(screen, dungeon_adv)
