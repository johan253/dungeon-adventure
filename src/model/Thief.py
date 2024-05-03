from src.model.Hero import Hero
from src.model.DungeonCharacter import DungeonCharacter
import random


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
        super().__init__(the_name, Thief.__name__)

    def do_special(self, other: DungeonCharacter) -> bool:
        """
        This method allows the thief to perform a special attack or ability.
        Uses a probability map to decide the outcome of a surprise attack.
        :param other: The monster to perform the special ability on.
        :return: True if an attack is attempted, False if caught.
        """
        attack_actions = {
            0.4: self.double_attack,  # 40% chance
            0.6: self.get_caught,  # 20% chance
            1.0: self.normal_attack  # 40% chance
        }

        outcome = random.random()
        for probability, action in sorted(attack_actions.items()):
            if outcome < probability:
                return action(other)

    def double_attack(self, other: DungeonCharacter) -> bool:
        print(f"{self.get_name()} launches a double attack on {other.get_name()}!")
        self.attack(other)  # First attack
        self.attack(other)  # Second attack
        return True

    def get_caught(self, other: DungeonCharacter) -> bool:
        print(f"{self.get_name()} is caught and cannot make an attack!")
        return False

    def normal_attack(self, other: DungeonCharacter) -> bool:
        print(f"{self.get_name()} performs a normal attack on {other.get_name()}.")
        self.attack(other)
        return True
