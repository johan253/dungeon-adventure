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
