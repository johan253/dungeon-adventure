import random
from src.model.RoomItem import RoomItem
from src.model.Directions import Direction


class Room:
    """
    Class representing a room in the dungeon. A room has items and doors.
    Attributes:
        - my_items: List[RoomItem]
            Represents the items in the room
        - my_doors: List[Direction]
            Represents the doors in the room
    """

    def __init__(self) -> None:
        """
        Constructor for the Room class
        """
        self.__my_items: [RoomItem] = RoomItem.list()
        self.__my_doors: [Direction] = Direction.list()

    def get_items(self) -> [RoomItem]:
        """
        Getter for the items in the room
        :return: the items in the room
        """
        return self.__my_items

    def get_doors(self) -> [Direction]:
        """
        Getter for the doors in the room
        :return: the doors in the room
        """
        return self.__my_doors

    def set_items(self, items: [RoomItem]) -> None:
        """
        Setter for the items in the room
        :param items: the new items in the room
        """
        self.__my_items = items

    def __str__(self) -> str:
        """
        String representation of the room
        :return: the string representation of the room
        """
        return "Room with items: " + str(self.__my_items) + " and doors: " + str(self.__my_doors)

    def generate_rooms(self):

        """
        Generates random items for the room
        """

        self.__my_items = []

        """
        (Possibly an) Exit - only one room will have an exit and 
        the room that contains the exit will contain NOTHING else
        """

        if is_exit:
            self.__my_items.append(RoomItem.Exit)
            return

        # Generate items

        for item in [RoomItem.HealingPotion, RoomItem.SpeedPotion , RoomItem.VisionPotion, RoomItem.Pit, RoomItem.BombPotion]:
            if random.randint(1, 100) <= 10:  # 10% chance
                self.__my_items.append(item)

        # Randomly add a pillar
        if random.randint(1, 100) <= 25:  # 25% chance
            self.__my_items.append(random.choice([RoomItem.PillarOfAbstraction, RoomItem.PillarOfEncapsulation, RoomItem.PillarOfInheritance, RoomItem.PillarOfPolymorphism]))
