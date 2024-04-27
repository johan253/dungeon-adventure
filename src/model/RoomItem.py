from enum import Enum


class RoomItem(Enum):
    """
    Enum for the different types of items that can be found in a room.
    """
    RoomItem = Enum('RoomItem', ['HealingPotion', 'VisionPotion', 'Pit', 'PillarOfAbstraction',
                                 'PillarOfEncapsulation', 'PillarOfInheritance', 'PillarOfPolymorphism',
                                 'Entrance', 'Exit'])
