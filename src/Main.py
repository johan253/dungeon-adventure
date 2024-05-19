from model.Dungeon import Dungeon

dungeon = Dungeon(4, 4)
print(dungeon)
x, y = dungeon.get_dimensions()
for i in range(x):
    for j in range(y):
        print(f"Room at ({i}, {j}): {dungeon.get_room(i, j)}")
        print(f"Items in room: {dungeon.get_room(i, j).get_items()}")
        print()
