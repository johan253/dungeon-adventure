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

    def test_character_attributes(self):
        """
        This method tests the attributes of the character classes
        """
        war = self.war
        self.assertEqual(war.get_name(), "warrior bob")
        self.assertEqual(war.get_class(), Warrior)
        war.set_health(25)
        self.assertEqual(war.get_health(), 25)
        self.assertLess(war.get_chance_to_block(), 1.0)
        self.assertLess(war.get_chance_to_hit(), 1.0)
        self.assertGreaterEqual(war.get_damage_min(), 0)

    def test_attack(self):
        """
        This method tests the general attack method
        """
        ogre = self.ogre
        war = self.war
        count_attack = 0
        count_miss = 0
        while ogre.get_health() > 0:
            health = ogre.get_health()
            war.attack(ogre)
            if ogre.get_health() != health:
                damage_dealt = health - ogre.get_health()
                self.assertGreaterEqual(damage_dealt, war.get_damage_min())
                self.assertLessEqual(damage_dealt, war.get_damage_max())
                count_miss += 1
            count_attack += 1
        self.assertEqual(ogre.get_health(), 0)
        self.assertGreater(count_attack, 0)
        self.assertGreaterEqual(count_miss, int(count_attack * war.get_chance_to_hit() * 0.5))
        self.assertLessEqual(count_miss, int(count_attack * war.get_chance_to_hit() * 1.5))

    # TODO: Implement the following test for every hero, when special abilities are implemented
    def test_special_ability_warrior(self):
        """
        This method tests the special ability of the warrior
        """
        pass

    def test_room_item(self):
        """
        This method tests the RoomItem enum
        """
        pass

    def test_room(self):
        """
        This method tests the Room class
        """
        pass

    def test_directions(self):
        """
        This method tests the Directions enum
        """
        pass

    def test_dungeon(self):
        """
        This method tests the Dungeon class
        """
        pass


if __name__ == '__main__':
    unittest.main()
