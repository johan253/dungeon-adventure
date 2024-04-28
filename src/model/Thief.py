from src.model.Hero import Hero
from src.model.Monster import Monster


class Thief(Hero):
    """
    This class represents a thief in the Dungeon Adventure game
    Attributes:
        - DEFAULT_NAME: String
            The default name of the thief
    """
    DEFAULT_NAME: str = "Thief"

    def __init__(self, the_name=DEFAULT_NAME) -> None:
        """
        Constructor for the Thief class
        :param the_name: The name of the thief
        """
        super().__init__(the_name, Thief)

    def do_special(self, other: Monster) -> bool:
        """
        This method allows the thief to perform a special attack or ability
        :param other: The monster to perform the special ability on
        :return: True if the special ability was successful, False otherwise
        """
        pass
