from src.model.Hero import Hero
from src.model.DungeonCharacter import DungeonCharacter
import random


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
    if random.random() <= 0.4:  # 40% chance to succeed
        damage = random.randint(75, 175)  # Corrected to use randint for a range of integers
        other.damage(damage)  # Assuming `damage` method processes damage and checks for character death
        print(f"{self.get_name()} successfully hits a Crushing Blow dealing {damage} damage!")
        return True
    else:
        print(f"{self.get_name()} failed to land a Crushing Blow.")
        return False