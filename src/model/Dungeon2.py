from collections import deque

from src.model.DugeonRoom import DungeonRoom
import random
from src.model.RoomItem import RoomItem


class Dungeon2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.my_root = DungeonRoom()
        self.entrance = None
        self.exit = None
        self.adventurer_location = None
        self.pillars = [RoomItem.PillarOfAbstraction, RoomItem.PillarOfEncapsulation,
                        RoomItem.PillarOfInheritance, RoomItem.PillarOfPolymorphism]

        self.__generate_dungeon()
        while not self.__valid():
            self.__generate_dungeon()
        self.place_items()

    def get_root(self) -> DungeonRoom:
        return self.my_root

    def __generate_dungeon(self):
        dungeon = [[DungeonRoom() for _ in range(self.width)] for _ in range(self.height)]
        for x, row in enumerate(dungeon):
            for y, room in enumerate(row):
                if random.random() < 0.30 and not room.get_north() and x > 0:
                    room.set_north(dungeon[x - 1][y])
                if random.random() < 0.30 and not room.get_south() and x < self.height - 1:
                    room.set_south(dungeon[x + 1][y])
                if random.random() < 0.30 and not room.get_east() and y < self.width - 1:
                    room.set_east(dungeon[x][y + 1])
                if random.random() < 0.30 and not room.get_west() and y > 0:
                    room.set_west(dungeon[x][y - 1])
        self.my_root = dungeon[0][0]

    def __valid(self):
        return self.check_room_number()

    def check_room_number(self):
        visited = set()
        self.dfs(self.my_root, visited)
        return len(visited) == self.width * self.height

    def dfs(self, root, visited):
        if root in visited:
            return
        visited.add(root)

        if root.get_east():
            self.dfs(root.get_east(), visited)
        if root.get_south():
            self.dfs(root.get_south(), visited)
        if root.get_west():
            self.dfs(root.get_west(), visited)
        if root.get_north():
            self.dfs(root.get_north(), visited)

    def place_items(self):
        self.entrance = self.my_root
        self.my_root.set_items([RoomItem.Entrance])
        self.adventurer_location = self.entrance

        while self.exit == self.entrance or not self.exit:
            self.exit = self.random_room()

        self.exit.set_items([RoomItem.Exit])

        # TODO: Fix placing pillars
        # Not placing all of items
        for pillar in self.pillars:
            placed = False
            while not placed:
                pillar_room = self.random_room()
                if pillar_room != self.entrance and pillar_room != self.exit:
                    existing_items = pillar_room.get_items()
                    if not any(item in self.pillars for item in existing_items):
                        pillar_room.set_items([pillar])
                        placed = True
                        print(f"Pillar {pillar} placed in {pillar_room}")

    def random_room(self) -> DungeonRoom:
        room = None
        while not room:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            room = self.get_room(self.my_root, x, y, set(), 0, 0)
        return room

    def get_room(self, root, x, y, visited, cur_x, cur_y):
        if not root or root in visited:
            return None
        visited.add(root)
        if x == cur_x and y == cur_y:
            return root
        return (self.get_room(root.get_north(), x, y, visited, cur_x, cur_y + 1) or
                self.get_room(root.get_south(), x, y, visited, cur_x, cur_y - 1) or
                self.get_room(root.get_east(), x, y, visited, cur_x + 1, cur_y) or
                self.get_room(root.get_west(), x, y, visited, cur_x - 1, cur_y))

    def __str__(self):
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
            string = (f"\n{"\t|" * num}ROOM: {num + 1} {"EXIT" if root == self.exit else ''}"
                      f"{"ENTRANCE" if root == self.entrance else ''}\n")
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

        x_dim, y_dim = get_x_y_dimensions(self.my_root, 0, 0)
        visited.clear()
        num_rooms = get_number_of_rooms(self.my_root)
        visited.clear()
        visual = visualize(self.my_root, 0)
        return (f"{num_rooms} rooms in the dungeon\n" +
                f"{x_dim} by {y_dim} dungeon\n"+
                f"visual:\n{visual}"
                f"Entrance: {self.entrance}\n"
                f"Exit: {self.exit}\n")
