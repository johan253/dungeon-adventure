from collections import deque
from src.model.DugeonRoom import DungeonRoom
import random
from src.model.RoomItem import RoomItem


class Dungeon:
    """
    Dungeon class that generates a dungeon with a random layout of rooms and places the entrance, exit, and pillars
    in random rooms.
    Attributes:
        __width (int): The width of the dungeon
        __height (int): The height of the dungeon
        __my_root (DungeonRoom): The root room of the dungeon
        __entrance (DungeonRoom): The entrance room of the dungeon
        __exit (DungeonRoom): The exit room of the dungeon
        __adventurer_location (DungeonRoom): The room the adventurer is currently in
        __pillars (list): The list of pillars that need to be placed in the dungeon
    """
    CHANCE_FOR_ROOM = 0.30
    MIN_DIMENSION = 3

    def __init__(self, width: int, height: int):
        """
        Constructor for the Dungeon class
        :param width: The width of the dungeon
        :param height: The height of the dungeon
        """
        if width < self.MIN_DIMENSION or height < self.MIN_DIMENSION:
            raise ValueError("Dungeon must be at least 4x4")
        self.__width = width
        self.__height = height
        self.__my_root = DungeonRoom()
        self.__entrance = None
        self.__exit = None
        self.__adventurer_location = None
        self.__pillars = [RoomItem.PillarOfAbstraction, RoomItem.PillarOfEncapsulation,
                          RoomItem.PillarOfInheritance, RoomItem.PillarOfPolymorphism]
        self.__generate_dungeon()
        while not self.__valid():
            self.__generate_dungeon()
        self.__place_items()

    def get_root(self) -> DungeonRoom:
        """
        Getter for the root room of the dungeon (the top left room)
        :return: The root room of the dungeon
        """
        return self.__my_root

    def __generate_dungeon(self) -> None:
        """
        Generates a random dungeon layout with rooms connected by doors at the root, given the width and height of the
        dungeon.
        """
        dungeon = [[DungeonRoom() for _ in range(self.__width)] for _ in range(self.__height)]
        for x, row in enumerate(dungeon):
            for y, room in enumerate(row):
                if random.random() < self.CHANCE_FOR_ROOM and not room.get_north() and x > 0:
                    room.set_north(dungeon[x - 1][y])
                if random.random() < self.CHANCE_FOR_ROOM and not room.get_south() and x < self.__height - 1:
                    room.set_south(dungeon[x + 1][y])
                if random.random() < self.CHANCE_FOR_ROOM and not room.get_east() and y < self.__width - 1:
                    room.set_east(dungeon[x][y + 1])
                if random.random() < self.CHANCE_FOR_ROOM and not room.get_west() and y > 0:
                    room.set_west(dungeon[x][y - 1])
        self.__my_root = dungeon[0][0]

    def __valid(self) -> bool:
        """
        Checks if the dungeon is valid by checking if all rooms are connected, within the bounds of the dungeon, and
        that all the necessary items are placed in the dungeon.
        :return: True if the dungeon is valid, False otherwise
        """
        return self.__check_room_number()

    def __check_room_number(self) -> bool:
        """
        Checks if the number of rooms in the dungeon is equal to the width * height of the dungeon
        :return: True if the number of rooms is equal to the width * height, False otherwise
        """
        visited = set()
        self.__dfs(self.__my_root, visited)
        return len(visited) == self.__width * self.__height

    def __dfs(self, root: DungeonRoom, visited: set) -> None:
        """
        Depth-first search to visit all rooms in the dungeon
        :param root: The current room being visited
        :param visited: The set of visited rooms
        """
        if root in visited:
            return
        visited.add(root)

        if root.get_east():
            self.__dfs(root.get_east(), visited)
        if root.get_south():
            self.__dfs(root.get_south(), visited)
        if root.get_west():
            self.__dfs(root.get_west(), visited)
        if root.get_north():
            self.__dfs(root.get_north(), visited)

    def __place_items(self) -> None:
        """
        Places the entrance, exit, and pillars in random rooms in the dungeon.
        """
        self.__entrance = self.__my_root
        self.__my_root.set_items([RoomItem.Entrance])
        self.__adventurer_location = self.__entrance

        while self.__exit == self.__entrance or not self.__exit:
            self.__exit = self.__random_room()

        self.__exit.set_items([RoomItem.Exit])

        for index in range(len(self.__pillars)):
            pillar = self.__pillars[index]
            placed = False

            while not placed:
                pillar_room = self.__random_room()
                if pillar_room != self.__entrance and pillar_room != self.__exit:
                    existing_items = pillar_room.get_items()
                    if not any(item in self.__pillars for item in existing_items):
                        pillar_room.set_items([pillar])
                        placed = True

    def __random_room(self) -> DungeonRoom:
        """
        Returns a random room in the dungeon
        :return: A random room in the dungeon
        """
        room: DungeonRoom | None = None
        x = 0
        y = 0
        while not room:
            x = random.randint(0, self.__width - 1)
            y = random.randint(0, self.__height - 1)
            room = self.__get_room(self.__my_root, x, y, set(), 0, 0)
        print(f"DEBUG: Random room selected from x: {x}, y: {y}")
        return room

    def __get_room(self, root: DungeonRoom, x: int, y: int, visited: set, cur_x: int, cur_y: int) -> DungeonRoom | None:
        """
        Helper function to get a room at a specific x, y coordinate in the dungeon
        :param root: The current room being visited
        :param x: The x coordinate of the room to find
        :param y: The y coordinate of the room to find
        :param visited: The set of visited rooms
        :param cur_x: The current x coordinate of the room being visited
        :param cur_y: The current y coordinate of the room being visited
        :return: The room at the x, y coordinate in the dungeon
        """
        if not root or root in visited:
            return None
        visited.add(root)
        if x == cur_x and y == cur_y:
            return root
        if root.get_east():
            temp = self.__get_room(root.get_east(), x, y, visited, cur_x + 1, cur_y)
            if temp:
                return temp
        if root.get_south():
            temp = self.__get_room(root.get_south(), x, y, visited, cur_x, cur_y + 1)
            if temp:
                return temp
        if root.get_west():
            temp = self.__get_room(root.get_west(), x, y, visited, cur_x - 1, cur_y)
            if temp:
                return temp
        if root.get_north():
            temp = self.__get_room(root.get_north(), x, y, visited, cur_x, cur_y - 1)
            if temp:
                return temp

    def __str__(self) -> str:
        """
        String representation of the dungeon
        :return: The string representation of the dungeon
        """
        visited = set()

        def get_number_of_rooms(root):
            if not root or root in visited:
                return 0
            visited.add(root)
            return (1 + get_number_of_rooms(root.get_north()) + get_number_of_rooms(root.get_south()) +
                    get_number_of_rooms(root.get_east()) + get_number_of_rooms(root.get_west()))

        def get_x_y_dimensions(root, x, y):
            if not root or root in visited:
                return 0, 0
            visited.add(root)
            max_x = x + 1
            max_y = y + 1
            for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                if dx == -1:
                    temp_x, temp_y = get_x_y_dimensions(root.get_west(), x - 1, y)
                    max_x, max_y = max(max_x, temp_x), max(max_y, temp_y)
                if dx == 1:
                    temp_x, temp_y = get_x_y_dimensions(root.get_east(), x + 1, y)
                    max_x, max_y = max(max_x, temp_x), max(max_y, temp_y)
                if dy == 1:
                    temp_x, temp_y = get_x_y_dimensions(root.get_south(), x, y + 1)
                    max_x, max_y = max(max_x, temp_x), max(max_y, temp_y)
                if dy == -1:
                    temp_x, temp_y = get_x_y_dimensions(root.get_north(), x, y - 1)
                    max_x, max_y = max(max_x, temp_x), max(max_y, temp_y)
            return max_x, max_y

        def visualize(root, num):
            if not root or root in visited:
                return ""
            visited.add(root)
            string = (f"\n{"\t|" * num}ROOM: {num + 1} {"EXIT" if root == self.__exit else ''}"
                      f"{"ENTRANCE" if root == self.__entrance else ''}\n")
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                if dy == -1:
                    string += f"|{"\t|" * (num + 1)}north: ({visualize(root.get_north(), num + 1)}|{"\t" * (num + 2)})\n"
                if dx == 1:
                    string += f"|{"\t|" * (num + 1)}east: ({visualize(root.get_east(), num + 1)}|{"\t" * (num + 2)})\n"
                if dy == 1:
                    string += f"|{"\t|" * (num + 1)}south: ({visualize(root.get_south(), num + 1)}|{"\t" * (num + 2)})\n"
                if dx == -1:
                    string += f"|{"\t|" * (num + 1)}west: ({visualize(root.get_west(), num + 1)}|{"\t" * (num + 2)})\n"
            return string

        x_dim, y_dim = get_x_y_dimensions(self.__my_root, 0, 0)
        visited.clear()
        num_rooms = get_number_of_rooms(self.__my_root)
        visited.clear()
        visual = visualize(self.__my_root, 0)
        return (f"{num_rooms} rooms in the dungeon\n" +
                f"{x_dim} by {y_dim} dungeon\n" +
                f"visual:\n{visual}"
                f"Entrance: {self.__entrance}\n"
                f"Exit: {self.__exit}\n")
