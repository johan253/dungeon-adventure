from enum import Enum
import random


class RoomItem(Enum):
    """
    Enum for the different types of items that can be found in a room.
    Attributes:
        - Entrance: str
            Represents the entrance to the dungeon
        - Exit: str
            Represents the exit to the dungeon
        - Pit: str
            Represents a pit in the room
        - HealingPotion: str
            Represents a healing potion in the room
        - VisionPotion: str
            Represents a vision potion in the room
        - PillarOfAbstraction: str
            Represents the pillar of abstraction in the room
        - PillarOfEncapsulation: str
            Represents the pillar of encapsulation in the room
        - PillarOfInheritance: str
            Represents the pillar of inheritance in the room
        - PillarOfPolymorphism: str
            Represents the pillar of polymorphism in the room

    """
    Entrance = "i"
    Exit = "O"
    Pit = "X"
    HealingPotion = "H"
    VisionPotion = "V"
    PillarOfAbstraction = "A"
    PillarOfEncapsulation = "E"
    PillarOfInheritance = "I"
    PillarOfPolymorphism = "P"
    BombPotion = "B"
    SpeedPotion = "S"

    @classmethod
    def list(cls) -> [str]:
        """
        Returns a list of the values of the RoomItem enum
        :return: a list of the values of the RoomItem enum
        """
        return list(map(lambda c: c.value, RoomItem))

    @classmethod
    def get_mixable_items(cls) -> [str]:
        """
        Returns a list of the values of the RoomItem enum that can be mixed
        :return: a list of the values of the RoomItem enum that can be mixed
        """
        return [RoomItem.HealingPotion, RoomItem.VisionPotion, RoomItem.Pit]

    @classmethod
    def get_pillars(cls) -> [str]:
        """
        Returns a list of the values of the RoomItem enum that are pillars
        :return: a list of the values of the RoomItem enum that are pillars
        """
        return [RoomItem.PillarOfAbstraction, RoomItem.PillarOfEncapsulation, RoomItem.PillarOfInheritance, RoomItem.PillarOfPolymorphism]

    @classmethod
    def get_static_items(cls) -> [str]:
        """
        Returns a list of the values of the RoomItem enum that are static and cannot be picked up by a player
        :return: a list of the values of the RoomItem enum that are static and cannot be picked up by a player
        """
        return [RoomItem.Entrance.value, RoomItem.Exit.value, RoomItem.Pit.value]
