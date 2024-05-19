from model.Dungeon import Dungeon

dungeon = Dungeon(3, 3)
print(dungeon)
print(dungeon.get_room(0, 0).get_items())