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

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_block: int) -> None:
        """
        Constructor for the Thief class
        :param the_name: The name of the thief
        :param the_health: The health of the thief
        :param the_min_damage: The minimum damage the thief can deal
        :param the_max_damage: The maximum damage the thief can deal
        :param the_attack_speed: The attack speed of the thief
        :param the_chance_to_hit: The chance to hit of the thief
        :param the_chance_to_block: The chance to block of the thief
        """
        if not any([the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                    the_chance_to_block]):
            raise ValueError("All parameters must be provided to create a Priestess")
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                         the_chance_to_block)

    def do_special(self, other: DungeonCharacter) -> bool:
        """
        This method allows the thief to perform a special attack or ability.
        Uses a probability map to decide the outcome of a surprise attack.
        :param other: The monster to perform the special ability on.
        :return: True if an attack is attempted, False if caught.
        """
        attack_actions = {
            0.4: self.__double_attack,  # 40% chance
            0.6: self.__get_caught,  # 20% chance
            1.0: self.__normal_attack  # 40% chance
        }

        outcome = random.random()
        for probability, action in sorted(attack_actions.items()):
            if outcome < probability:
                return action(other)

    def __double_attack(self, other: DungeonCharacter) -> bool:
        """
        This method allows the thief to perform a double attack on another character.
        :param other: The character to attack
        :return: True if the attack was successful, False otherwise
        """
        # print(f"{self.get_name()} launches a double attack on {other.get_name()}!")
        res1 = self.attack(other)  # First attack
        res2 = self.attack(other)  # Second attack
        return res1 or res2

    def __get_caught(self, other: DungeonCharacter) -> bool:
        """
        This method allows the thief to attempt a surprise attack but gets caught.
        :param other: The character to attack
        :return: False, as the thief is caught and cannot make an attack
        """
        # print(f"{self.get_name()} is caught and cannot make an attack!")
        return False

    def __normal_attack(self, other: DungeonCharacter) -> bool:
        """
        This method allows the thief to perform a normal attack on another character.
        :param other: The character to attack
        :return: True if the attack was successful, False otherwise
        """
        # print(f"{self.get_name()} performs a normal attack on {other.get_name()}.")
        return self.attack(other)
