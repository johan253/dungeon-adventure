import random
from src.model.DugeonRoom import DungeonRoom


class Dungeon2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.my_root = DungeonRoom()

        self.entrance = None
        self.exit = None
        self.pillars = None

        self.generate_dungeon(self.my_root, 0, 0)
        self.place_items()  # place the entrance, exit and pillars

    def generate_dungeon(self, root, x, y):
        """
        Maze generating algorithm (im unsure about implementation details, but Rooms
		Will have some sort of “North, E, S, W” property for you to check those
        """
        pass
    def place_items(self):
        """
        Randomly place the entrance, exit and pillars in the dungeon
        """
        pass

    def __str__(self):
        """ Provide a string representation of the dungeon's main features for debugging. """
        return (f"Dungeon dimensions: {self.my_width}x{self.my_height}\n"
                f"Entrance located at: {self.entrance}\n"
                f"Exit located at: {self.exit}\n"
                f"Pillars located at: {self.pillars}")