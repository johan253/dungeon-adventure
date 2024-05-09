from controller.DungeonAdventure import DungeonAdventure
from model.Warrior import Warrior
from model.Thief import Thief
from model.Priestess import Priestess
import pygame
from SaveLoadManager import SaveLoadSystem
from View import MainMenu

pygame.init()


saveLoadManager = SaveLoadSystem(".save", "save_data")


MainMenu = MainMenu()



print("Welcome to Dungeon Adventure!")
print("Please enter your name:")
name = input()
print("Please choose a class:")
print("1. Warrior")
print("2. Thief")
print("3. Priestess")
choice = input("Enter the number of the class you want to play: ")
valid = choice in ["1", "2", "3"]
while not valid:
    print("Invalid input. Please enter a number between 1 and 3.")
    choice = input("Enter the number of the class you want to play: ")
    valid = choice in ["1", "2", "3"]
player_type: type = None
if choice == "1":
    player_type = Warrior
elif choice == "2":
    player_type = Thief
else:
    player_type = Priestess

print(f"Welcome, {name} the {player_type.__name__}!")
game: DungeonAdventure = DungeonAdventure(name, player_type)
while True:
    print("Enter one of the following choices")
    print("1. Move North")
    print("2. Move South")
    print("3. Move East")
    print("4. Move West")
    print("5. QUIT GAME")

    direction = input("Enter the number of the direction you want to move: ")
    valid = direction in ["1", "2", "3", "4", "5"]
    while not valid:
        print("Invalid input. Please enter a number between 1 and 4.")
        direction = input("Enter the number of the direction you want to move: ")
        valid = direction in ["1", "2", "3", "4", "5"]
        is_dead = False
    if direction == "1":
        is_dead = game.move_player(0, -1)
    elif direction == "2":
        is_dead = game.move_player(0, 1)
    elif direction == "3":
        is_dead = game.move_player(1, 0)
    elif direction == "4":
        is_dead = game.move_player(-1, 0)
    else:
        break
    if is_dead:
        print("Game Over, you have died.")
        break
print("Thank you for playing Dungeon Adventure!")
