from enum import Enum

#Directions enum

class Directions(Enum):
    NORTH = 'North'
    EAST  = 'East'
    SOUTH = 'South'
    WEST = 'West'

# RoomItem enumeration

class RoomItem(Enum):
    HEALING_POTION = 'HealingPotion'
    VISION_POTION = 'VisionPotion'
    PIT = 'Pit'
    ABSTRACTION = 'Abstraction'
    ENCAPSULATION = 'Encapsulation'
    INHERITANCE = 'Inheritance'
    POLYMORPHISM = 'Polymorphism'
    ENTRANCE = 'Entrance'
    EXIT = 'Exit'


# Room class with myItems and myDoors attributes, and various
class Room:
    def __init__self(self):
        self.myItems = []
        self.myDoors = []

    def get_items(self):
        return self.myItems

    def get_doors(self):
        return self.myDoors

    def to_string(self):
        pass

    def set_items(self,items):
        self.myItems = items
