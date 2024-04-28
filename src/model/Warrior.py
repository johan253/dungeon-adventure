from src.model.Hero import Hero
from src.model.DungeonCharacter import DungeonCharacter


class Warrior(Hero):
    """
    This class represents a warrior in the Dungeon Adventure game
    Attributes:
        - DEFAULT_NAME: String
            The default name of the warrior
    """
    DEFAULT_NAME: str = "Warrior"

    def __init__(self, the_name=DEFAULT_NAME) -> None:
        """
        Constructor for the Warrior class
        :param the_name: The name of the warrior
        """
        super().__init__(the_name, Warrior)

    def do_special(self, other: DungeonCharacter) -> bool:
        """
        This method allows the warrior to perform a special attack or ability
        :param other: The monster to perform the special ability on
        :return: True if the special ability was successful, False otherwise
        """
        pass
