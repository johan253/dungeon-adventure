from model.DugeonRoom import DungeonRoom
from model.RoomItem import RoomItem
import random


class Dungeon:
    """
    Dungeon class that generates a dungeon with a random layout of rooms and places the entrance, exit, and pillars
    in random rooms.
    Attributes:
        CHANCE_FOR_ROOM (float): The chance that a room will be generated
            in any direction of another room in the dungeon
        MIN_DIMENSION (int): The minimum dimension of the dungeon for the x and y-axis
        __width (int): The width of the dungeon
        __height (int): The height of the dungeon
        __root (DungeonRoom): The root room of the dungeon
        __entrance (DungeonRoom): The entrance room of the dungeon
        __exit (DungeonRoom): The exit room of the dungeon
    """
    CHANCE_FOR_ROOM = 0.30
    MIN_DIMENSION = 4

    def __init__(self, the_width: int, the_height: int) -> None:
        """
        Constructor for the Dungeon class
        :param the_width: The width of the dungeon
        :param the_height: The height of the dungeon
        """
        if the_width < self.MIN_DIMENSION or the_height < self.MIN_DIMENSION:
            raise ValueError("Dungeon must be at least 4x4")
        self.__width: int = the_width
        self.__height: int = the_height
        self.__root: DungeonRoom | None = DungeonRoom()
        self.__entrance: DungeonRoom | None = None
        self.__exit: DungeonRoom | None = None
        self.__generate_dungeon()
        while not self.__valid():
            self.__generate_dungeon()
        self.__place_items()
        while not self.__check_items():
            self.__place_items()

    def get_dimensions(self) -> tuple[int, int]:
        """
        Getter for the dimensions of the dungeon
        :return: The dimensions of the dungeon
        """
        return self.__width, self.__height

    def get_root(self) -> DungeonRoom:
        """
        Getter for the root room of the dungeon (the top left room)
        :return: The root room of the dungeon
        """
        return self.__root

    def get_room(self, the_x: int, the_y: int) -> DungeonRoom:
        """
        Returns a room at a specific x, y coordinate in the dungeon
        :return: A random room in the dungeon
        """
        if the_x < 0 or the_x >= self.__width or the_y < 0 or the_y >= self.__height:
            raise ValueError("Invalid x or y coordinate")
        result = self.__get_room_helper(self.__root, the_x, the_y, set(), 0, 0)
        return result if result else ArithmeticError("Room not found")

    def get_exit(self) -> DungeonRoom:
        """
        Getter for the exit room of the dungeon
        :return: The exit room of the dungeon
        """
        return self.__exit

    def __get_room_helper(self, root: DungeonRoom, target_x: int, target_y: int, visited: set, cur_x: int, cur_y: int)\
            -> DungeonRoom | None:
        """
        Helper function to get a room at a specific x, y coordinate in the dungeon
        :param root: The current room being visited
        :param target_x: The x coordinate of the room to find
        :param target_y: The y coordinate of the room to find
        :param visited: The set of visited rooms
        :param cur_x: The current x coordinate of the room being visited
        :param cur_y: The current y coordinate of the room being visited
        :return: The room at the x, y coordinate in the dungeon
        """
        if not root or root in visited:
            return None
        visited.add(root)
        if target_x == cur_x and target_y == cur_y:
            return root
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for index, room in enumerate(root.get_all_adjacent_rooms()):
            dx, dy = directions[index]
            result = self.__get_room_helper(room, target_x, target_y, visited, cur_x + dx, cur_y + dy)
            if result:
                return result
        return None

    def __place_items(self) -> None:
        """
        Places the entrance, exit, and pillars in random rooms in the dungeon.
        """
        # TODO: Possibly make entrance randomly placed as well
        self.__entrance = self.__root
        self.__entrance.set_items([RoomItem.Entrance])
        self.__entrance.set_monster(None)

        # Get all rooms in the dungeon, filter out the entrance, and randomly place the exit and pillars
        all_rooms = set()
        self.__dfs(self.__root, all_rooms)
        valid_rooms = [room for room in all_rooms if room != self.__entrance]
        random.shuffle(valid_rooms)

        self.__exit = valid_rooms.pop()
        self.__exit.set_items([RoomItem.Exit])
        self.__exit.set_monster(None)

        for pillar in RoomItem.get_pillars():
            valid_rooms.pop().set_items([pillar])

    def __generate_dungeon(self) -> None:
        """
        Generates a dungeon with a random layout of rooms and connects them with each other. Uses a disjoint set data
        structure to connect the rooms using Kruskal's algorithm.
        """
        dungeon = [[DungeonRoom() for _ in range(self.__width)] for _ in range(self.__height)]
        edges = []
        equivalency = {}
        for x, row in enumerate(dungeon):
            for y, room in enumerate(row):
                for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                    if 0 <= x + dx < self.__width and 0 <= y + dy < self.__height:
                        # Add all the plausible edges to the list
                        edges.append( ((room, x, y), (dungeon[x + dx][y + dy], x + dx, y + dy)) )
                equivalency[room] = room

        # Shuffle the edges to randomize the dungeon
        random.shuffle(edges)

        def find(the_room: DungeonRoom) -> DungeonRoom:
            """
            Find the parent of the room. Used to find the parent of a room in the disjoint set data structure.
            :param the_room: The room to find the parent of
            :return: The parent of the room
            """
            if the_room != equivalency[the_room]:
                equivalency[the_room] = find(equivalency[the_room])
            return equivalency[the_room]

        def union(r1: DungeonRoom, r2: DungeonRoom):
            """
            Unites two rooms in the disjoint set data structure
            :param r1: The first room to unite
            :param r2: The second room to unite
            """
            equivalency[find(r1)] = find(r2)

        connections = 0
        # Connect the rooms using Kruskal's algorithm
        while connections < self.__width * self.__height - 1:
            (room1, x1, y1), (room2, x2, y2) = edges.pop()
            # If the rooms are not connected by the same set, connect them
            if find(room1) != find(room2):
                union(room1, room2)
                connections += 1
                # Determine the direction of the rooms and connect them
                if x1 == x2:
                    if y1 < y2:
                        room1.set_south(room2)
                        room2.set_north(room1)
                    else:
                        room1.set_north(room2)
                        room2.set_south(room1)
                else:
                    if x1 < x2:
                        room1.set_east(room2)
                        room2.set_west(room1)
                    else:
                        room1.set_west(room2)
                        room2.set_east(room1)

        self.__root = dungeon[0][0]

    def __valid(self) -> bool:
        """
        Checks if the dungeon is valid by checking if all rooms are connected and within the bounds of the dungeon.
        :return: True if the dungeon is valid, False otherwise
        """
        return self.__check_room_number() and self.__check_dimensions(self.__root, set(), 0, 0)

    def __check_room_number(self) -> bool:
        """
        Checks if the number of rooms in the dungeon is equal to the width * height of the dungeon
        :return: True if the number of rooms is equal to the width * height, False otherwise
        """
        visited = set()
        self.__dfs(self.__root, visited)
        return len(visited) == self.__width * self.__height

    def __check_dimensions(self, root: DungeonRoom, visited: set, cur_x: int, cur_y: int) -> bool:
        """
        Checks if the dimensions of the dungeon are correct
        :param root: The current room being visited
        :param visited: The set of visited rooms
        :param cur_x: The current x coordinate of the room being visited
        :param cur_y: The current y coordinate of the room being visited
        :return: True if the dimensions are correct, False otherwise
        """
        if not root or root in visited:
            return True
        visited.add(root)
        if cur_x >= self.__width or cur_y >= self.__height or cur_x < 0 or cur_y < 0:
            return False
        for dx, dy in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            if dx == -1:
                if not self.__check_dimensions(root.get_west(), visited, cur_x - 1, cur_y):
                    return False
            if dx == 1:
                if not self.__check_dimensions(root.get_east(), visited, cur_x + 1, cur_y):
                    return False
            if dy == 1:
                if not self.__check_dimensions(root.get_south(), visited, cur_x, cur_y + 1):
                    return False
            if dy == -1:
                if not self.__check_dimensions(root.get_north(), visited, cur_x, cur_y - 1):
                    return False
        return True

    def __check_items(self) -> bool:
        """
        Checks if all the necessary items are placed in the dungeon
        :return: True if all the necessary items are placed, False otherwise
        """
        visited = set()
        self.__dfs(self.__root, visited)
        all_items: list[RoomItem] = [item for room in visited for item in room.get_items()]
        return all(pillar in all_items for pillar in RoomItem.get_pillars()) and RoomItem.Entrance in all_items and \
            RoomItem.Exit in all_items

    def __dfs(self, root: DungeonRoom, visited: set) -> None:
        """
        Depth-first search to visit all rooms in the dungeon. Used to add all rooms to the visited set.
        :param root: The current room being visited
        :param visited: The set of visited rooms
        """
        if root in visited:
            return
        visited.add(root)
        for room in root.get_all_adjacent_rooms():
            if room:
                self.__dfs(room, visited)

    def __str__(self):
        """
        String representation of the dungeon and its rooms
        :return: The string representation of the dungeon
        """
        string = "*" + "**" * self.__width + "\n"
        for row in range(self.__height):
            string += "*"
            bottom_string = "*"
            for col in range(self.__width):
                room = self.get_room(col, row)
                item_char = ' '

                if len(room.get_items()) > 1:
                    item_char = 'M'
                elif len(room.get_items()) == 1:
                    item_char = room.get_items()[0].value

                string += f"{item_char}"

                if room.get_east():
                    string += "|"
                else:
                    string += "*"

                if room.get_south():
                    bottom_string += "-*"
                else:
                    bottom_string += "**"

            string += "\n"
            string += bottom_string + "\n"
        return string
