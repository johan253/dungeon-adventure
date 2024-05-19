import unittest
from src.model.DugeonRoom import DungeonRoom
from src.model.RoomItem import RoomItem
from src.model.Dungeon import Dungeon


class DungeonTest(unittest.TestCase):

    def setUp(self) -> None:
        """
        This method is called before each test. It initializes all the characters
        """
        self.room = DungeonRoom()
        self.dungeon = Dungeon(Dungeon.MIN_DIMENSION, Dungeon.MIN_DIMENSION)

    def test_dungeon_constructor(self):
        """
        This method tests the dungeon class
        """
        self.dungeon = Dungeon(5, 5)
        self.assertTrue(self.dungeon.get_dimensions() == (5, 5), "Dungeon dimensions not set correctly")
        root = self.dungeon.get_root()
        visited = set()

        def dfs(room):
            """
            This method performs a depth first search on the dungeon
            :param room:
            :return:
            """
            if room is None:
                return
            visited.add(room)
            for adjacent in room.get_all_adjacent_rooms():
                if adjacent not in visited:
                    dfs(adjacent)

        self.assertTrue(root is not None, "Root room not set")
        dfs(root)
        self.assertTrue(len(visited) == 25, "Dungeon not initialized correctly")
        visited.clear()
        root = Dungeon(7, 4).get_root()
        dfs(root)
        self.assertTrue(len(visited) == 28, "Dungeon not initialized correctly")
        for i in range(Dungeon.MIN_DIMENSION):
            for j in range(Dungeon.MIN_DIMENSION):
                self.assertRaises(ValueError, Dungeon, i, j)

    def test_dungeon_necessary_items(self):
        """
        This method tests that the dungeon has the necessary items
        """
        visited = set()

        def dfs(the_room):
            """
            This method performs a depth first search on the dungeon
            :param the_room:
            :return:
            """
            if the_room is None:
                return
            visited.add(the_room)
            for adjacent in the_room.get_all_adjacent_rooms():
                if adjacent not in visited and adjacent is not None:
                    dfs(adjacent)

        root = self.dungeon.get_root()
        dfs(root)
        all_items: set[RoomItem] = set()
        for room in visited:
            for item in room.get_items():
                all_items.add(item)
        self.assertTrue(all(pillar in all_items for pillar in RoomItem.get_pillars()), "Pillars not in dungeon")
        self.assertTrue(RoomItem.Entrance in all_items, f"Entrance not in dungeon")
        self.assertTrue(RoomItem.Exit in all_items, "Exit not in dungeon")

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
        self.room.set_items([RoomItem.VisionPotion])
        items = self.room.get_items()
        self.assertTrue(items == [RoomItem.VisionPotion], "Item not added to room")

        self.room.set_items(RoomItem.list())
        items = self.room.get_items()
        self.assertTrue(items == RoomItem.list(), "Items not added to room")

        self.room.set_items([])
        self.assertTrue(self.room.get_items() == [], "Items not added to room")

    def test_dungeon_room_remove_item(self):
        """
        This method tests the remove item method of the dungeon room
        """
        self.room.set_items(RoomItem.list())

        self.room.remove_item(RoomItem.VisionPotion)
        items = self.room.get_items()
        self.assertTrue((RoomItem.VisionPotion != item for item in items), "Item not removed from room")

        self.room.set_items(RoomItem.list())
        for item in RoomItem.get_mixable_items():
            self.room.remove_item(item)
        self.assertTrue(any(RoomItem.get_mixable_items()) not in self.room.get_items(), "Items not removed from room")

    def test_dungeon_room_adjacent_rooms(self):
        """
        This method tests the adjacent rooms of the dungeon room
        """
        north = DungeonRoom()
        east = DungeonRoom()
        south = DungeonRoom()
        west = DungeonRoom()
        self.room.set_items(RoomItem.list())
        self.room.set_north(north)
        self.room.set_east(east)
        self.room.set_south(south)
        self.room.set_west(west)

        self.assertTrue(self.room.get_all_adjacent_rooms() == [self.room.get_north(), self.room.get_east(),
                                                               self.room.get_south(), self.room.get_west()],
                        "Adjacent rooms not returned correctly")
        self.assertTrue(self.room.get_north() == north, "North room not returned correctly")
        self.assertTrue(self.room.get_east() == east, "East room not returned correctly")
        self.assertTrue(self.room.get_south() == south, "South room not returned correctly")
        self.assertTrue(self.room.get_west() == west, "West room not returned correctly")

        self.room = DungeonRoom()
        self.assertTrue(self.room.get_all_adjacent_rooms() == [None, None, None, None],
                        "Adjacent rooms not returned correctly")
        self.room.set_south(DungeonRoom())
        self.assertTrue(self.room.get_all_adjacent_rooms() == [None, None, self.room.get_south(), None],
                        "Adjacent rooms not returned correctly")
