import unittest

from model.DungeonCharacter import DungeonCharacter
from model.Hero import Hero
from model.Monster import Monster
from model.Skeleton import Skeleton
from model.Ogre import Ogre
from model.Gremlin import Gremlin
from model.Warrior import Warrior
from model.Thief import Thief
from model.Priestess import Priestess

from model.Room import Room
from model.RoomItem import RoomItem
from model.Directions import Direction


class TestModels(unittest.TestCase):
    """
    This class tests the model classes
    """

    def setUp(self) -> None:
        """
        This method is called before each test. It initializes all the characters
        """
        self.war: Warrior = Warrior("warrior bob")
        self.thi: Thief = Thief("thief joe")
        self.pri: Priestess = Priestess("priest alice")

        self.ogre: Ogre = Ogre("Shrek")
        self.skeleton: Skeleton = Skeleton("Bones")
        self.gremlin: Gremlin = Gremlin("Gizmo")

    def test_abstract_character_instantiation(self):
        """
        This method tests that the abstract classes cannot be instantiated
        """
        self.assertRaises(TypeError, DungeonCharacter, "bob", DungeonCharacter,
                          "Should not be able to instantiate DungeonCharacter directly")
        self.assertRaises(TypeError, Hero, "bob", Hero,
                          "Should not be able to instantiate Hero directly")
        self.assertRaises(TypeError, Monster, "bob", Monster,
                          "Should not be able to instantiate Monster directly")

    def test_dungeon_character_attributes(self):
        """
        This method tests the attributes of the character classes
        """
        war = self.war
        self.assertEqual(war.get_name(), "warrior bob",
                         "Name should be instantiated with given value")
        self.assertEqual(war.get_category(), "Hero",
                         "Warrior category should be 'Hero'")
        war.set_health(25)
        self.assertEqual(war.get_health(), 25,
                         "Health setter should set health to given value")
        self.assertLess(war.get_chance_to_block(), 1.0,
                        "Chance to block should be less than 1.0")
        self.assertLess(war.get_chance_to_hit(), 1.0,
                        "Chance to hit should be less than 1.0")
        self.assertGreaterEqual(war.get_damage_min(), 0,
                                "Minimum damage should be greater than or equal to 0")

    def test_attack(self):
        """
        This method tests the general attack method
        """
        other_character = self.thi
        war = self.war
        count_attack = 0
        count_miss = 0
        while other_character.get_health() > 0:
            health = other_character.get_health()
            war.attack(other_character)
            if other_character.get_health() != health and other_character.get_health() > 0:
                damage_dealt = health - other_character.get_health()
                self.assertGreaterEqual(damage_dealt, war.get_damage_min(),
                                        "Damage dealt should be greater than or equal to minimum damage")
                self.assertLessEqual(damage_dealt, war.get_damage_max(),
                                     "Damage dealt should be less than or equal to maximum damage")
                count_miss += 1
            count_attack += 1
        self.assertEqual(other_character.get_health(), 0, "Other character health should be 0 when dead")
        self.assertGreater(count_attack, 0, "Should have attacked at least once")
        self.assertGreaterEqual(count_miss, int(count_attack * war.get_chance_to_hit() * 0.5),
                                f"Should have hit at least about {int(count_attack * war.get_chance_to_hit())} times")
        self.assertLessEqual(count_miss, int(count_attack * war.get_chance_to_hit() * 1.5),
                             f"Should have hit at most about {int(count_attack * war.get_chance_to_hit())} times")

    def test_chance_to_block(self):
        """
        This method tests the chance to block an attack
        """
        thief = self.thi
        count_block = 0
        count_attacks = 0
        while thief.get_health() > 0:
            health = thief.get_health()
            thief.damage(5)
            if thief.get_health() == health:
                count_block += 1
            count_attacks += 1
        self.assertEqual(thief.get_health(), 0, "Warrior health should be 0 when dead")
        self.assertGreater(count_block, 0, "Should have blocked at least once")
        self.assertGreaterEqual(count_block, int(count_attacks * thief.get_chance_to_block() * 0.5),
                                f"Should have been hit at least about {int(count_block * thief.get_chance_to_block())} times")
        self.assertLessEqual(count_block, int(count_attacks * thief.get_chance_to_block() * 1.5),
                             f"Should have been hit at most about {int(count_block * thief.get_chance_to_block())} times")

    # TODO: Implement the following test for every hero, when special abilities are implemented
    def test_special_ability_warrior(self):
        """
        This method tests the special ability of the warrior
        """
        pass

    def test_room_items(self):
        """
        This method tests the RoomItem enum
        """
        all_items: list[str] = RoomItem.list()
        for string in ("A", "E", "I", "P", "i", "O", "X", "H", "V", "B", "S"):
            self.assertIn(string, all_items, f"Item {string} not found in RoomItem enum")
            all_items.remove(string)
        self.assertEqual(len(all_items), 0, "RoomItem enum has extra values")

    def test_directions(self):
        """
        This method tests the Directions enum
        """
        all_directions: list[int] = Direction.list()
        for direction in (1, 2, 3, 4):
            self.assertIn(direction, all_directions, f"Direction {direction} not found in Directions enum")
            all_directions.remove(direction)
        self.assertEqual(len(all_directions), 0, "Directions enum has extra values")

    # TODO: Implement the following tests for the Room and Dungeon classes when they are implemented
    def test_room(self):
        """
        This method tests the Room class
        """
        pass

    def test_dungeon(self):
        """
        This method tests the Dungeon class
        """
        pass


if __name__ == '__main__':
    unittest.main()
