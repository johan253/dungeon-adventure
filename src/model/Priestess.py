from src.model.Hero import Hero
from src.model.Monster import Monster


class Priestess(Hero):
    """
    This class represents a priestess in the Dungeon Adventure game
    Attributes:
        - DEFAULT_NAME: String
            The default name of the priestess
    """
    DEFAULT_NAME: str = "Priestess"

    def __init__(self, the_name=DEFAULT_NAME) -> None:
        """
        Constructor for the Priestess class
        :param the_name: The name of the priestess
        """
        super().__init__(the_name, Priestess)

    def do_special(self, other) -> bool:
        """
        This method allows the priestess to perform a special attack or ability
        :param other: The monster to perform the special ability on
        :return: True if the special ability was successful, False otherwise
        """
        pass
