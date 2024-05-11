from src.model.DugeonRoom import DungeonRoom
import random


class Dungeon2:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.my_root = DungeonRoom()
        self.entrance = None
        self.exit = None
        self.adventurer_location = None
        self.pillars = ["Abstraction", "Inheritance", "Polymorphism", "Encapsulation"]

        self.generate_dungeon()
        self.ensure_transferability()

    def generate_dungeon(self):
        def connect_rooms(room1, room2, dr, dc):
            if room1 and room2:
                if dr == -1 and room1.get_north() is None and room2.get_south() is None:
                    room1.set_north(room2)
                    room2.set_south(room1)
                elif dr == 1 and room1.get_south() is None and room2.get_north() is None:
                    room1.set_south(room2)
                    room2.set_north(room1)
                elif dc == 1 and room1.get_east() is None and room2.get_west() is None:
                    room1.set_east(room2)
                    room2.set_west(room1)
                elif dc == -1 and room1.get_west() is None and room2.get_east() is None:
                    room1.set_west(room2)
                    room2.set_east(room1)

        def dfs(room, row, col):
            visited[row][col] = True
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # East, South, West, North
            random.shuffle(directions)
            for dr, dc in directions:
                next_row, next_col = row + dr, col + dc
                if 0 <= next_row < self.height and 0 <= next_col < self.width and not visited[next_row][next_col]:
                    next_room = DungeonRoom()
                    connect_rooms(room, next_room, dr, dc)
                    dfs(next_room, next_row, next_col)

        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        dfs(self.my_root, 0, 0)

        while self.my_root.get_north():
            self.my_root = self.my_root.get_north()
        while self.my_root.get_west():
            self.my_root = self.my_root.get_west()

    def ensure_transferability(self):
        self.place_items()
        while not self.check_maze_completeness(self.my_root):
            self.my_root = DungeonRoom()
            self.generate_dungeon()
            self.place_items()

    def check_maze_completeness(self, root):
        visited = set()
        self.dfs(root, visited)
        print(f"Visited rooms: {len(visited)}")
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
        self.adventurer_location = self.entrance

        while self.exit == self.entrance or not self.exit:
            self.exit = self.random_room()


        placed_pillars = set()
        for pillar in self.pillars:
            while True:
                pillar_room = self.random_room()
                if pillar_room != self.entrance and pillar_room != self.exit and pillar_room not in placed_pillars:
                    placed_pillars.add(pillar)
                    break

    def random_room(self):
        x = random.randint(0, self.width - 1)
        y = random.randint(0, self.height - 1)
        return self.get_room(self.my_root, x, y, set(), 0, 0)

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
        # string = "*"
        # prev_row = []
        # current: DungeonRoom = self.my_root
        # while current:
        #     string += "**" if not current.get_north() else "-*"
        #     current = current.get_east()
        # string += "\n"
        # current = self.my_root
        # while current:
        #     first = current
        #     string += "*"
        #     bottom = "*"
        #     while current:
        #         string += " |" if current.get_east() else " *"
        #         bottom += "-*" if current.get_south() else "**"
        #         current = current.get_east()
        #     string += "\n" + bottom + "\n"
        #     current = first.get_south()
        # return string
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
