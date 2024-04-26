from enum import Enum


class RoomItem(Enum):
    RoomItem = Enum('RoomItem', ['HealingPotion', 'VisionPotion', 'Pit', 'PillarOfAbstraction',
                                 'PillarOfEncapsulation', 'PillarOfInheritance', 'PillarOfPolymorphism',
                                 'Entrance', 'Exit'])
