import random

'''This class represents a room in the dungeon. Additionally, 
    it stores information about the room' properties.

@author Aly Badr, Johan Hernandez, Lwazi Mabota
'''


class DungeonRoom:

    SPAWN_CHANCE = 0.1

    '''
    Constructor for Dungeon Room.
    Takes parameters: x, y, has_visual_potion, has_health_potion, monster_encountered, has_visited, has_pillar'''
    def __init__(self, x, y, has_visual_potion=None, has_health_potion=None,
                 monster_encountered=None, has_visited=None, has_pillar=None):
        self.x = x
        self.y = y
        self.my_room = None
        self.my_type = "basic"
        self.has_visual_potion = has_visual_potion if has_visual_potion is not None else random.random()
        self.has_health_potion = has_health_potion if has_health_potion is not None else random.random()
        self.monster_encountered = monster_encountered if monster_encountered is not None else False
        self.has_visited = has_visited if has_visited is not None else False
        self.has_pillar = has_pillar if has_pillar is not None else False
        self.my_monster_type = "none"

    '''
    Setter for the my_room property.'''
    def set_room(self, num):
        self.my_room = f"Dungeon Room {num}.tmx"
    '''
    Setter for the my_type property.
    Depending on the provided type properties of the room may change.'''
    def set_type(self, the_type):
        self.my_type = the_type
        if the_type in {"entrance", "exit"}:
            self.set_visual_potion(False)
            self.set_health_potion(False)
            self.set_monster_type(False)
        elif the_type == "pillar":
            self.set_visual_potion(False)
            self.set_health_potion(False)

    def has_visual_potion(self):
        return self.has_visual_potion

    def set_visual_potion(self, visual_potion):
        self.has_visual_potion = visual_potion

    def has_health_potion(self):
        return self.has_health_potion

    def set_health_potion(self, health_potion):
        self.has_health_potion = health_potion

    def has_monster_type(self):
        return self.my_monster_type

    def set_monster_type(self, monster_type):
        self.my_monster_type = monster_type

    def get_monster_type(self):
        return self.my_monster_type

    def has_visited(self):
        return self.has_visited

    def set_visited(self, visited):
        self.has_visited = visited

    def has_pillar(self):
        return self.has_pillar

    def set_pillar(self, pillar):
        self.has_pillar = pillar

    '''
    String representation of the room'''
    def __str__(self):
        room_str = "|++++++|\n"

        for i in range(2):
            cur_line = "|      |\n"
            if i == 0 and self.has_health_potion():
                cur_line = cur_line[:5] + 'H' + cur_line[6:]
            if i == 0 and self.monster_encountered():
                cur_line = cur_line[:1] + 'M' + cur_line[2:]
            if i == 1 and self.has_visual_potion():
                cur_line = cur_line[:2] + 'V' + cur_line[2:]
            if i == 1 and self.has_health_potion():
                cur_line = cur_line[:5] + 'H' + cur_line[6:]
            room_str += cur_line
        room_str += "|++++++|"
        return room_str
