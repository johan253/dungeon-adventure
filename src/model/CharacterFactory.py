from src.model.DungeonCharacter import DungeonCharacter
from src.model.Skeleton import Skeleton
from src.model.Ogre import Ogre
from src.model.Gremlin import Gremlin
from src.model.Warrior import Warrior
from src.model.Thief import Thief
from src.model.Priestess import Priestess
from src.controller.DatabaseController import DatabaseController


class CharacterFactory:
    """
    This class is responsible for creating characters in the game.
    """
    __DB: DatabaseController = DatabaseController()
    GREMLIN = "Gremlin"
    OGRE = "Ogre"
    SKELETON = "Skeleton"
    THIEF = "Thief"
    WARRIOR = "Warrior"
    PRIESTESS = "Priestess"

    @staticmethod
    def create_character(char_name: str, user_name: str) -> DungeonCharacter:
        """
        This method creates a character based on the specified name.
        :param char_name: The name of the character
        :param user_name: The name of the user
        :return: A character object
        """
        char = None
        if char_name == CharacterFactory.GREMLIN:
            char = Gremlin(user_name)
        elif char_name == CharacterFactory.OGRE:
            char = Ogre(user_name)
        elif char_name == CharacterFactory.SKELETON:
            char = Skeleton(user_name)
        elif char_name == CharacterFactory.THIEF:
            char = Thief(user_name)
        elif char_name == CharacterFactory.WARRIOR:
            char = Warrior(user_name)
        elif char_name == CharacterFactory.PRIESTESS:
            char = Priestess(user_name)
        else:
            raise ValueError("Invalid character name")
        return char
