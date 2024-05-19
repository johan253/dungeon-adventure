from random import random
from model.DungeonCharacter import DungeonCharacter
from model.Dungeon import Dungeon
from model.CharacterFactory import CharacterFactory


class DungeonAdventure:
    """
    This class is the controller for the Dungeon Adventure game. It is responsible for managing the player, the dungeon,
    and the inventory. It also handles the movement of the player and the use of items.
    Attributes:
        - __my_player (Player): The player object
        - __my_inventory (List[RoomItem]): The inventory of the player
        - __my_dungeon (Dungeon): The dungeon object
    """

    def __init__(self, player_name: str, player_class: str):
        """
        This method initializes the Dungeon Adventure game.
        :param player_name: The name of the player
        :param player_class: The class of the player
        """
        print("DA: Initializing Game...")
        self.__my_player = CharacterFactory().create_character(player_class, player_name)
        print("DA: \n", self.__my_player)
        self.__my_inventory = []  # RoomItem
        self.__my_dungeon = Dungeon(5, 5)  # Dungeon
        self.locations = {self.__my_player: self.__my_dungeon.get_root()} # keys are instances and values are currrent rooms
        # dungeon

    def move_player(self, direction) -> bool:
        """
            This method moves the player in the specified direction.
            :param direction: The direction to move ('north', 'south', 'east', 'west')
            :return: True if the move was successful and False otherwise.
        """
        current_room = self.locations[self.__my_player]
        next_room = getattr(current_room, f'get_{direction}')()

        if next_room is None:
            print(f"DA: No room with {direction}")

        self.locations[self.__my_player] = next_room
        print(f"Moved{direction} to a new room.")

        if random() <= 0.5:
            monster = CharacterFactory().create_random_monster(self.__my_player.get_name())
            if not self.__battle(self.__my_player, monster):
                print("Battle lost or fled.")
                self.locations[self.__my_player] = current_room  # Optionally move back
                return False
        return True

    def use_item(self, item) -> bool:  # item = Room-Item
        """
        This method uses the specified item.
        :param item: The item to use
        :return: True if the item was used successfully, False otherwise
        """
        current_room = self.locations[self.__my_player]  # Access current room from the ma


    def __battle(self, char1: DungeonCharacter, char2: DungeonCharacter) -> bool:
        """
        This method handles a battle between two characters.
        :param char1: One of the characters
        :param char2: The other character
        :return: TBD
        """
        print("You encountered a monster!")
        print("You must battle it to proceed.\n")
        while char1.get_health() > 0 and char2.get_health() > 0:
            prev_hero_health = char1.get_health()
            prev_monster_health = char2.get_health()
            print(f"{char1}\n{char2}\n")
            print("Enter one of the following choices")
            print("1. Attack")
            print("2. Attempt to flee")
            battle_choice = input("Enter the number of the action you want to take: ")
            valid = battle_choice in ["1", "2"]
            while not valid:
                print("Invalid input. Please enter a number between 1 and 2.")
                battle_choice = input("Enter the number of the action you want to take: ")
                valid = battle_choice in ["1", "2"]
            if battle_choice == "1":
                print("You attack the monster!\n")
                char1.attack(char2)
            else:
                if random() <= 0.5:
                    print("You successfully fled the battle!\n")
                    return False
                else:
                    print("You failed to flee the battle!\n")
            char2.attack(char1)
            print(f"{char1.get_name()} took {prev_hero_health - char1.get_health()} damage.")
            print(f"{char2.get_name()} took {prev_monster_health - char2.get_health()} damage.\n")
        # To be implemented
        if not self.__my_player.get_health() <= 0:
            print("You defeated the monster!")
            return False
        else:
            return True

    def get_dungeon(self):
        """
        This method returns the dungeon object.
        :return: The dungeon object
        """
        return self.__my_dungeon

    def reset_dungeon(self, dim):
        """
        This method resets the dungeon object.
        """
        self.__my_dungeon = Dungeon(dim, dim)

    def get_inventory(self):
        """
        This method returns the inventory of the player.
        :return: The inventory of the player
        """
        return self.__my_inventory

    def get_state(self):
        """
        This method returns the state of current game.
        :return: The state of the game
        """
        return [self.__my_player, self.__my_inventory, self.__my_dungeon]

    def add_item_to_inventory(self, item):
        """
        Adds an item to the player's inventory
        :param item: the iden to be added to the inventory
        :return: None
        """
        self.__my_inventory.append(item)
        print(f"Added {item.name} to the inventory.")

