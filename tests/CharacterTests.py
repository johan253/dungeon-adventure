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


class CharacterTests(unittest.TestCase):
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
                                f"Should have been hit at least about "
                                f"{int(count_block * thief.get_chance_to_block())} times")
        self.assertLessEqual(count_block, int(count_attacks * thief.get_chance_to_block() * 1.5),
                             f"Should have been hit at most about "
                             f"{int(count_block * thief.get_chance_to_block())} times")

    def test_monster_chance_to_heal(self):
        """
        This method tests the chance to heal for monsters
        """
        gremlin = self.gremlin
        count_heal = 0
        count_attacks = 0
        while gremlin.get_health() > 0:
            health = gremlin.get_health()
            gremlin.damage(5)
            if gremlin.get_health() >= health:
                count_heal += 1
            count_attacks += 1
        self.assertEqual(gremlin.get_health(), 0, "Ogre health should be 0 when dead")
        self.assertGreater(count_heal, 0, "Should have healed at least once")
        self.assertGreaterEqual(count_heal, int(count_attacks * gremlin.get_chance_to_heal() * 0.5),
                                f"Should have healed at least about "
                                f"{int(count_heal * gremlin.get_chance_to_heal())} times")
        self.assertLessEqual(count_heal, int(count_attacks * gremlin.get_chance_to_heal() * 1.5),
                             f"Should have healed at most about "
                             f"{int(count_heal * gremlin.get_chance_to_heal())} times")

    # TODO: Implement the following test for every hero, when special abilities are implemented
    def test_special_ability_warrior(self):
        """
        This method tests the special ability of the warrior
        """
        war = self.war
        ogre = self.ogre
        count_special = 0
        count_attacks = 0
        while ogre.get_health() > 0:
            health = ogre.get_health()
            success = war.do_special(ogre)
            if success and ogre.get_health() > 0:
                self.assertLess(ogre.get_health(), health,
                                "Ogre health should decrease after special ability lands")
                self.assertGreaterEqual(health - ogre.get_health(), 75,
                                        "Ogre health should decrease by at least 75")
                self.assertLessEqual(health - ogre.get_health(), 175,
                                     "Ogre health should decrease by at most 175")
                count_special += 1
            count_attacks += 1
        self.assertEqual(ogre.get_health(), 0, "Ogre health should be 0 when dead")
        self.assertGreater(count_special, 0, "Should have used special ability at least once")
        self.assertGreaterEqual(count_special, int(count_attacks * 0.4 * 0.5),
                                f"Should have used special ability at least about "
                                f"{int(count_special * 0.4)} times")
        self.assertLessEqual(count_special, int(count_attacks * 0.4 * 1.5),
                             f"Should have used special ability at most about "
                             f"{int(count_special * 0.4)} times")

    def test_special_ability_thief(self):
        """
        This method tests the special ability of the thief
        """
        thi = self.thi
        ogre = self.ogre
        count_special = 0
        count_attempts = 0
        for i in range(100):
            thi = Thief("thief joe")
            ogre = Ogre("Shrek")
            health = ogre.get_health()
            thi.do_special(ogre)
            result = health > ogre.get_health()
            print(count_special)
            if result:
                count_special += 1
            count_attempts += 1
        self.assertTrue(0.75 * thi.get_chance_to_hit() * count_attempts <= count_special <=
                        0.85 * count_attempts * thi.get_chance_to_hit(),
                        f"Special ability landed {count_special} times out of {count_attempts} attempts")


    def test_special_ability_priestess(self):
        """
        This method tests the special ability of the priestess
        """
        pass


if __name__ == '__main__':
    unittest.main()
