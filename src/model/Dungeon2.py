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
        # self.ensure_transferability()
        # self.place_items()

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
        while not self.check_maze_completeness(self.my_root):
            self.my_root = DungeonRoom()
            self.generate_dungeon()

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

    def place_items(self):
        self.entrance = self.my_root
        self.adventurer_location = self.entrance

        while True:
            exit_room = self.random_room()
            if exit_room != self.entrance:
                self.exit = exit_room
                break

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
        return self.get_room(x, y)

    def get_room(self, x, y):
        # Implement a method to retrieve room at (x, y).
        pass

    def __str__(self):
        string = "*"
        prev_row = []
        current: DungeonRoom = self.my_root
        while current:
            string += "**" if not current.get_north() else "-*"
            current = current.get_east()
        string += "\n"
        current = self.my_root
        while current:
            first = current
            string += "*"
            bottom = "*"
            while current:
                string += " |" if current.get_east() else " *"
                bottom += "-*" if current.get_south() else "**"
                current = current.get_east()
            string += "\n" + bottom + "\n"
            current = first.get_south()
        return string

