import unittest
from src.model.DugeonRoom import DungeonRoom
from src.model.RoomItem import RoomItem
# from src.model.Dungeon import Dungeon


class DungeonTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        This method is called before each test. It initializes all the characters
        """
        self.room = DungeonRoom()
        # TODO: Add Dungeon class and its tests when it is implemented
        # self.dungeon = Dungeon()

    def test_dungeon_room_constructor(self):
        """
        This method tests the dungeon class
        """
        count_rooms = 0
        count_rooms_with_item = 0
        for i in range(100):
            room = DungeonRoom()
            count_rooms += 1
            if len(room.get_items()) > 0:
                count_rooms_with_item += 1

        self.assertTrue(count_rooms * 0.075 * len(RoomItem.get_mixable_items()) < count_rooms_with_item <
                        count_rooms * 0.125 * len(RoomItem.get_mixable_items()),
                        f"Room item distribution is incorrect, out of 100 rooms, {count_rooms_with_item} have items")

    def test_dungeon_room_set_item(self):
        """
        This method tests the add item method of the dungeon room
        """
        self.room.set_items(RoomItem.VisionPotion)
        items = self.room.get_items()
        self.assertTrue(items == RoomItem.VisionPotion, "Item not added to room")

        self.room.set_items(RoomItem.list())
        items = self.room.get_items()
        self.assertTrue(items == RoomItem.list(), "Items not added to room")

    def test_dungeon_room_remove_item(self):
        """
        This method tests the remove item method of the dungeon room
        """
        self.room.set_items(RoomItem.list())

        self.room.remove_item(RoomItem.VisionPotion)
        items = self.room.get_items()
        self.assertTrue((RoomItem.VisionPotion != item for item in items), "Item not removed from room")
