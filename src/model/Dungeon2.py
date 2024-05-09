import random
from src.model.DugeonRoom import DungeonRoom


class Dungeon2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.my_root = DungeonRoom()

        self.entrance = False
        self.exit = False
        self.Abstraction = None
        self.Inheritance = None
        self.Polymorphism = None
        self.Encapsulation = None

        self.generate_dungeon(self.my_root, 0, 0)
        self.place_items()  # place the entrance, exit and pillars

    def generate_dungeon(self, root, x, y):
        """
        Maze generating algorithm (im unsure about implementation details, but Rooms
		Will have some sort of “North, E, S, W” property for you to check those
        """
        # Start at the root of the Dungeon

        # First check if the dungeon is out of bounds:

        if x >= self.width or y >= self.height:
            return

        # Establish the East link if passing out of bounds
        if x + 1 < self.width and not root.east:
            root.east = DungeonRoom()
            root.east.west = root  # Link the connection between west and east to root
            self.generate_dungeon(root.__east, x + 1, y)

            # Establish the East link if passing out of bounds
            if y + 1 < self.width and not root.south:
                root.south = DungeonRoom()
                root.south.north = root  # Link the connection between west and east to root
                self.generate_dungeon(root.__south, x, y + 1)

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
