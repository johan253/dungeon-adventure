from src.model.DungeonCharacter import DungeonCharacter
from src.model.Hero import Hero
from src.model.Monster import Monster
from src.model.Skeleton import Skeleton
from src.model.Ogre import Ogre
from src.model.Gremlin import Gremlin
from src.model.Warrior import Warrior
from src.model.Thief import Thief
from src.model.Priestess import Priestess
from src.controller.DatabaseController import DatabaseController
from random import choice


class CharacterFactory:
    """
    This class is responsible for creating characters in the game.
    """
    GREMLIN = "Gremlin"
    OGRE = "Ogre"
    SKELETON = "Skeleton"
    THIEF = "Thief"
    WARRIOR = "Warrior"
    PRIESTESS = "Priestess"

    def __init__(self):
        """
        Constructor for the CharacterFactory class
        """
        self.__DB = DatabaseController()

    def create_character(self, character_class: str, user_name: str) -> Monster | Hero:
        """
        This method creates a character based on the character class and username.
        :param character_class: The class of the character
        :param user_name: The name of the user
        :return: The character object
        """
        if not character_class.strip() or not user_name.strip():
            raise ValueError("Character class or user name cannot be empty.")

        if character_class == self.GREMLIN:
            return self.__get_monster(Gremlin, user_name)
        elif character_class == self.OGRE:
            return self.__get_monster(Ogre, user_name)
        elif character_class == self.SKELETON:
            return self.__get_monster(Skeleton, user_name)
        elif character_class == self.THIEF:
            return self.__get_hero(Thief, user_name)
        elif character_class == self.WARRIOR:
            return self.__get_hero(Warrior, user_name)
        elif character_class == self.PRIESTESS:
            return self.__get_hero(Priestess, user_name)
        else:
            raise ValueError("Invalid character class.")

    def create_random_monster(self, user_name: str) -> Monster:
        """
        This method creates a random monster for the user
        :param user_name: The name of the user
        :return: The monster object
        """
        return self.create_character(choice([self.GREMLIN, self.OGRE, self.SKELETON]), user_name)

    def __get_monster(self, char_type: type, user_name: str) -> Monster:
        """
        This method retrieves a monster from the database
        :param char_type: The type of the monster
        :param user_name: The name of the user
        :return: The monster object
        """
        data = self.__DB.get_stats("Monster", char_type.__name__)
        return char_type(user_name,
                         data[self.__DB.HEALTH],
                         data[self.__DB.MIN_DAMAGE],
                         data[self.__DB.MAX_DAMAGE],
                         data[self.__DB.ATTACK_SPEED],
                         data[self.__DB.CHANCE_TO_HIT],
                         data[self.__DB.CHANCE_TO_HEAL],
                         data[self.__DB.MIN_HEAL],
                         data[self.__DB.MAX_HEAL])

    def __get_hero(self, char_type: type, user_name: str) -> Hero:
        """
        This method retrieves a hero from the database
        :param char_type: The type of the hero
        :param user_name: The name of the user
        :return: The hero object
        """
        data = self.__DB.get_stats("Hero", char_type.__name__)
        return char_type(user_name,
                         data[self.__DB.HEALTH],
                         data[self.__DB.MIN_DAMAGE],
                         data[self.__DB.MAX_DAMAGE],
                         data[self.__DB.ATTACK_SPEED],
                         data[self.__DB.CHANCE_TO_HIT],
                         data[self.__DB.CHANCE_TO_BLOCK])
