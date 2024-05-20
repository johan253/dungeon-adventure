from model.Dungeon import Dungeon
from model.CharacterFactory import CharacterFactory

dungeon = Dungeon(4, 4)
print(dungeon)

random_char = CharacterFactory().create_character(CharacterFactory.PRIESTESS)
print(random_char)

