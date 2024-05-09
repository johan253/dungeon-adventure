import random


"""
This class represents a Dungeon with rooms of a certain size.
Every time the dungeon is created there is an entrance, exit, pillar rooms, and possibility of monsters spawning.
@author Aly Badr, Johan Hernandez, Lwazi Mabota"""


class DungeonRoom:

    """
    This function is the constructor of a Dungeon Room.
    The parameters are the various properties of the room that are possible to spawn."""

    def __init__(self, x, y, has_encountered_monster=False, has_visited_room=False, has_pillar=False,
                 has_vision_potion=False, has_heal_potion=False):
        self.type = "basic"
        self.x = x
        self.y = y
        self.has_encountered_monster = has_encountered_monster
        self.has_visited_room = has_visited_room
        self.has_pillar = has_pillar
        self.has_vision_potion = has_vision_potion
        self.has_heal_potion = has_heal_potion

    """This function sets the type of the dungeon room(entrance, exit, or pillar room)"""
    def set_type(self, room_type):
        self.type = room_type
    """This function sets whether the room has been visited or not."""
    def set_visited(self, visited):
        self.has_visited_room = visited
    """This function sets whether the room contains a pillar or not."""
    def set_pillar(self, has_pillar):
        self.has_pillar = has_pillar
    """The function sets whether a monster has been encountered or not."""
    def encountered_monster(self):
        return self.has_encountered_monster

    class Dungeon:
        """Constructor for the Dungeon class.
        Initializes the dungeon of a width and height as a 2D list that function as the dungeon layout with
        an entrance and exit."""
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.dungeon = [[0 for _ in range(height)] for _ in range(width)]
            self.entrance = None
            self.exit = None
        """This function generates the layout of the dungeon starting from a random position.
        In addition, this function sets the entrance and exit and rooms containing pillars."""
        def generate_dungeon(self):
            self.generate_dungeon(0, 0)
            self._set_entrance()
            self._set_exit()
            self._set_pillar_rooms()
        """The helper function generates the dungeon at a specified x and y position."""

        def _generate_dungeon(self, x, y):
            direction = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(direction)
            for dx, dy in direction:
                next_x, next_y = x + dx, y + dy
                if 0 <= next_x < self.width and 0 <= next_y < self.height and self.dungeon[next_x][next_y] == 0:
                    self.dungeon[x][y] |= 1 << direction.index((dx, dy))
                    self.dungeon[next_x][next_y] |= 1 << direction.index((-dx, -dy))
                    self._generate_dungeon(next_x, next_y)
        """Sets the entrance of the dungeon at a random position."""
        def _set_entrance(self):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.entrance = DungeonRoom(x, y)
            self.entrance.set_type("entrance")
        """"Sets the exit of the dungeon at a random position."""
        def _set_exit(self):
            for _ in range(15):
                x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
                if self.dungeon[x][y] == 0:
                    self.exit = DungeonRoom(x, y)
                    self.exit.set_type("exit")
                    break
        """Sets the pillar of the dungeon at a random position."""
        def _set_pillar_rooms(self):
            for _ in range(4):
                for _ in range(15):
                    x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
                    if self.dungeon[x][y] == 0:
                        self.dungeon[x][y] = DungeonRoom(x, y)
                        self.dungeon[x][y].set_type("pillar_room")
                        break
        """This function returns a string representation of the dungeon(dungeon layout, rooms, monsters, potions
        and pillars"""
        def __str__(self):
            dungeon_str = ""

            for y in range(self.height):
                for x in range(self.width):
                    dungeon_str += "+------" if self.dungeon[x][y] == 0 else "+       "
                dungeon_str += "+\n"

                for _ in range(2):
                    for x in range(self.width):
                        cur_line = "|     " if self.dungeon[x][y] == 0 else "      "
                        if _ == 0 and self.dungeon[x][y].has_monster:
                            cur_line = cur_line[:1] + "monster" + cur_line[2:]
                        if _ == 0 and self.dungeon[x][y].has_heal_potion:
                            cur_line = cur_line[:6] + "heal" + cur_line[7:]
                        if _ == 1 and self.dungeon[x][y].has_vision_potion:
                            cur_line = cur_line[:1] + "vision" + cur_line[2:]
                        if _ == 1 and self.dungeon[x][y].has_pillar:
                            cur_line = cur_line[:6] + "pillar" + cur_line[7:]
                        dungeon_str += cur_line
                    dungeon_str += "|\n"
            dungeon_str += "+------" * self.width + "+"
            return dungeon_str
