from src.model.Hero import Hero
from src.model.DungeonCharacter import DungeonCharacter
import random


class Priestess(Hero):
    """
    This class represents a priestess in the Dungeon Adventure game
    Attributes:
        - DEFAULT_NAME: String
            The default name of the priestess
    """
    DEFAULT_NAME: str = "Priestess"

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_block: int) -> None:
        """
        Constructor for the Priestess class
        :param the_name: The name of the priestess
        :param the_health: The health of the priestess
        :param the_min_damage: The minimum damage the priestess can deal
        :param the_max_damage: The maximum damage the priestess can deal
        :param the_attack_speed: The attack speed of the priestess
        :param the_chance_to_hit: The chance to hit of the priestess
        :param the_chance_to_block: The chance to block of the priestess
        """
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                         the_chance_to_block)

    def do_special(self, other: DungeonCharacter = None) -> bool:
        """
        This method allows the priestess to perform a special healing ability.
        It can heal herself or another character. If no target is specified, it heals herself.
        :param other: The character to perform the healing on (defaults to None, which means heal self)
        :return: True if the healing was performed, False otherwise (e.g., if the target is already at full health)
        """
        target = other if other is not None else self
        current_health = target.get_health()
        max_health = 100  # Assuming 100 is the max health limit; adjust as needed for your game design
        if current_health < max_health:
            heal_amount = random.randint(25, 50)  # Heal range
            new_health = min(max_health, current_health + heal_amount)
            target.set_health(new_health)
            print(f"{target.get_name()} healed for {heal_amount} health points to {new_health}.")
            return True
        else:
            print(f"{target.get_name()} is already at full health.")
            return False


