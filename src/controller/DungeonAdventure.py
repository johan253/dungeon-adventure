class DungeonAdventure:
    """
    This class is the controller for the Dungeon Adventure game. It is responsible for managing the player, the dungeon,
    and the inventory. It also handles the movement of the player and the use of items.
    Attributes:
        - __my_player (Player): The player object
        - __my_inventory (List[RoomItem]): The inventory of the player
        - __my_dungeon (Dungeon): The dungeon object
    """
    def __init__(self, player_name: str, player_class: type):
        """
        This method initializes the Dungeon Adventure game.
        :param player_name: The name of the player
        :param player_class: The class of the player
        """
        print("Initializing Game...")
        self.__my_player = player_class(player_name)
        print(self.__my_player)
        self.__my_inventory = []  # RoomItem
        self.__my_dungeon = None  # Dungeon

    def move_player(self, dx, dy) -> bool:
        """
        This method moves the player in the specified direction.
        :param dx: The change in x-coordinate
        :param dy: The change in y-coordinate
        :return:
        """
        print()
        if dy == -1:
            print("Moving North")
        elif dy == 1:
            print("Moving South")
        elif dx == 1:
            print("Moving East")
        elif dx == -1:
            print("Moving West")
        else:
            raise ValueError("Invalid direction")
        print()
        # To be implemented
        return True

    def use_item(self, item) -> bool:  # item = Room-Item
        """
        This method uses the specified item.
        :param item: The item to use
        :return: True if the item was used successfully, False otherwise
        """
        pass

    def __battle(self, char1, char2):
        """
        This method handles a battle between two characters.
        :param char1: One of the characters
        :param char2: The other character
        :return: TBD
        """
        pass

    def get_dungeon(self):
        """
        This method returns the dungeon object.
        :return: The dungeon object
        """
        return self.__my_dungeon

    def get_inventory(self):
        """
        This method returns the inventory of the player.
        :return: The inventory of the player
        """
        return self.__my_inventory



