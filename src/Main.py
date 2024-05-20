from src.controller.DungeonAdventure import DungeonAdventure
from src.model.CharacterFactory import CharacterFactory

game = DungeonAdventure("Johan", CharacterFactory.WARRIOR)

print("Welcome to Dungeon Adventure!")
print("W. Move North")
print("S. Move South")
print("D. Move East")
print("A. Move West")
choice_move = input("Enter your choice: ")
while True:
    if choice_move.upper() == "W":
        game.move_player("north")
    elif choice_move.upper() == "S":
        game.move_player("south")
    elif choice_move.upper() == "D":
        game.move_player("east")
    elif choice_move.upper() == "A":
        game.move_player("west")
    else:
        print("Invalid input")
    print(game.get_dungeon())
    choice_move = input("Enter your choice: ")
