from model.Hero import Hero
from model.DungeonCharacter import DungeonCharacter
import random


class Warrior(Hero):
    """
    This class represents a warrior in the Dungeon Adventure game
    Attributes:
        - DEFAULT_NAME: String
            The default name of the warrior
    """
    DEFAULT_NAME: str = "Warrior"

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_block: int) -> None:
        """
        Constructor for the Warrior class
        :param the_name: The name of the warrior
        :param the_health: The health of the warrior
        :param the_min_damage: The minimum damage the warrior can deal
        :param the_max_damage: The maximum damage the warrior can deal
        :param the_attack_speed: The attack speed of the warrior
        :param the_chance_to_hit: The chance to hit of the warrior
        :param the_chance_to_block: The chance to block of the warrior
        """
        if not any([the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                    the_chance_to_block]):
            raise ValueError("All parameters must be provided to create a Priestess")
        if the_name.strip() == "":
            the_name = self.DEFAULT_NAME
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                         the_chance_to_block)

    def do_special(self, other: DungeonCharacter) -> bool:
        """
        This method allows the warrior to perform a special attack or ability
        :param other: The monster to perform the special ability on
        :return: True if the special ability was successful, False otherwise
        """
        if random.random() <= 0.4:  # 40% chance to succeed
            damage = random.randint(75, 175)  # Corrected to use randint for a range of integers
            other.damage(damage)  # Assuming `damage` method processes damage and checks for character death
            return True
        else:
            return False
