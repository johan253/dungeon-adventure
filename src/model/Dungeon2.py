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

        self.generate_dungeon(self.my_root, 0, 0)
        self.ensure_transferability()
        self.place_items()

    def generate_dungeon(self, root, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return

        if x + 1 < self.width and not root.get_east():
            east_room = DungeonRoom()
            root.set_east(east_room)
            east_room.set_west(root)
            self.generate_dungeon(east_room, x + 1, y)

        if y + 1 < self.height and not root.get_south():
            south_room = DungeonRoom()
            south_room.set_north(root)
            self.generate_dungeon(south_room, x, y + 1)

    def ensure_transferability(self):
        while not self.check_maze_completeness(self.my_root):
            self.my_root = DungeonRoom()
            self.generate_dungeon(self.my_root, 0, 0)

    def check_maze_completeness(self, root):
        visited = set()
        queue = [root]
        directions = ['get_north', 'get_east', 'get_south', 'get_west']

        while queue:
            current_room = queue.pop(0)
            if current_room not in visited:
                visited.add(current_room)
                for direction in directions:
                    adjacent_room = getattr(current_room, direction)()
                    if adjacent_room and adjacent_room not in visited:
                        queue.append(adjacent_room)

        total_rooms = self.width * self.height
        return len(visited) == total_rooms

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
        return (f"Dungeon dimensions: {self.width}x{self.height}\n"
                f"Entrance located at: {self.entrance}\n"
                f"Exit located at: {self.exit}\n"
                f"Pillars: {', '.join(self.pillars)}\n"
                f"Adventurer's current location: {self.adventurer_location}")
