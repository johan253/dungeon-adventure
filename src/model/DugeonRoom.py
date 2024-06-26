import random
from src.model.CharacterFactory import CharacterFactory
from src.model.Monster import Monster
from src.model.RoomItem import RoomItem
from typing import TypeVar

T = TypeVar('T', bound='DungeonRoom')


class DungeonRoom:
    """
    A class that represents a room in the dungeon.
    Attributes:
        - __items (List[RoomItem]): The items in the room
        - __monster (Monster): The monster in the room
        - __north (DungeonRoom): The room to the north
        - __east (DungeonRoom): The room to the east
        - __south (DungeonRoom): The room to the south
        - __west (DungeonRoom): The room to the west
    """

    SPAWN_CHANCE = 0.15

    def __init__(self):
        """
        Constructor for DungeonRoom
        """
        self.__items: list[RoomItem] = []
        for item in RoomItem.get_mixable_items():
            if random.random() < DungeonRoom.SPAWN_CHANCE:
                self.__items.append(item)
        self.__monster: Monster | None = None
        if random.random() < DungeonRoom.SPAWN_CHANCE:
            self.__monster = CharacterFactory().create_random_monster()
        self.__north: DungeonRoom | None = None
        self.__east: DungeonRoom | None = None
        self.__south: DungeonRoom | None = None
        self.__west: DungeonRoom | None = None

    def get_monster(self) -> Monster | None:
        """
        Getter for the monster in the room
        :return: the monster in the room
        """
        if self.__monster and not self.__monster.is_alive():
            self.__monster = None
        return self.__monster

    def set_monster(self, monster: Monster | None) -> None:
        """
        Setter for the monster in the room
        :param monster: the monster in the room
        """
        self.__monster = monster

    def get_items(self) -> list[RoomItem]:
        """
        Getter for the items in the room
        :return: the items in the room
        """
        return self.__items

    def set_items(self, items: list[RoomItem]) -> None:
        """
        Setter for the items in the room
        :param items: the items in the room
        """
        self.__items = items

    def remove_item(self, item: RoomItem) -> bool:
        """
        Removes an item from the room if it is present
        :param item: the item to remove
        :return: True if the item was removed, False otherwise
        """
        if item not in self.__items:
            return False
        self.__items.remove(item)
        return True

    def get_all_adjacent_rooms(self) -> list[T]:
        """
        Returns a list of all adjacent rooms. Guaranteed to be in the order [north, east, south, west] even
        if a room is None.
        :return: a list of all adjacent rooms
        """
        return [self.__north, self.__east, self.__south, self.__west]

    def get_north(self) -> T | None:
        """
        Getter for the room to the north
        :return: the room to the north
        """
        return self.__north

    def set_north(self, room: T | None):
        """
        Setter for the room to the north
        :param room: the room to the north
        """
        self.__north = room
        if room:
            room.__south = self

    def get_east(self) -> T | None:
        """
        Getter for the room to the east
        :return: the room to the east
        """
        return self.__east

    def set_east(self, room: T | None):
        """
        Setter for the room to the east
        :param room: the room to the east
        """
        self.__east = room
        if room:
            room.__west = self

    def get_south(self) -> T | None:
        """
        Getter for the room to the south
        :return: the room to the south
        """
        return self.__south

    def set_south(self, room: T | None):
        """
        Setter for the room to the south
        :param room: the room to the south
        """
        self.__south = room
        if room:
            room.__north = self

    def get_west(self) -> T | None:
        """
        Getter for the room to the west
        :return: the room to the west
        """
        return self.__west

    def set_west(self, room: T | None):
        """
        Setter for the room to the west
        :param room: the room to the west
        """
        self.__west = room
        if room:
            room.__east = self

    def __str__(self) -> str:
        """
        String representation of the room
        :return: the string representation of the room
        """
        item_char = ' '
        if len(self.__items) > 1:
            item_char = 'M'
        elif len(self.__items) == 1:
            item_char = self.__items[0].value

        north = '*' if self.__north is None else '-'
        east = '*' if self.__east is None else '|'
        south = '*' if self.__south is None else '-'
        west = '*' if self.__west is None else '|'

        return f"*{north}*\n" \
               f"{west}{item_char}{east}\n" \
               f"*{south}*"
