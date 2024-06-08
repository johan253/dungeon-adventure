from src.model.DungeonCharacter import DungeonCharacter
from random import random
from abc import ABC


class Monster(DungeonCharacter, ABC):
    """
    This class represents a monster in the Dungeon Adventure game
    Attributes:
        - my_chance_to_heal: Float
            The chance that the monster will heal itself
    """

    def __new__(cls, *args, **kwargs):
        """
        This method overrides the __new__ method to prevent instantiation of the abstract Monster class
        :param args: The arguments to pass to the constructor
        :param kwargs: The keyword arguments to pass to the constructor
        :return: The new instance of the Monster class
        """
        if cls is Monster:
            raise TypeError("The Monster class may not be instantiated directly")
        return super().__new__(cls)

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_heal: int,
                 the_min_heal: int, the_max_heal: int) -> None:
        """
        Constructor for the Monster class
        :param the_name: The name of the monster
        :param the_health: The health of the monster
        :param the_min_damage: The minimum damage the monster can deal
        :param the_max_damage: The maximum damage the monster can deal
        :param the_attack_speed: The attack speed of the monster
        :param the_chance_to_hit: The chance to hit of the monster
        :param the_chance_to_heal: The chance that the monster will heal itself
        :param the_min_heal: The minimum amount that the monster can heal
        :param the_max_heal: The maximum amount that the monster can heal

        """
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit)
        self.__my_chance_to_heal: float = the_chance_to_heal
        self.__my_min_heal: int = the_min_heal
        self.__my_max_heal: int = the_max_heal

    def get_chance_to_heal(self) -> float:
        """
        This method returns the chance that the monster will heal itself
        :return: The chance that the monster will heal itself
        """
        return self.__my_chance_to_heal

    def get_min_heal(self) -> int:
        """
        This method returns the minimum amount that the monster can heal
        :return: The minimum amount that the monster can heal
        """
        return self.__my_min_heal

    def get_max_heal(self) -> int:
        """
        This method returns the maximum amount that the monster can heal
        :return: The maximum amount that the monster can heal
        """
        return self.__my_max_heal

    def heal(self) -> None:
        """
        This method heals the monster based on chance to heal and healing range
        """
        if random() <= self.__my_chance_to_heal:
            heal_amount = int(random() * (self.__my_max_heal - self.__my_min_heal) + self.__my_min_heal)
            self.set_health(min(self.get_health() + heal_amount, self.get_max_health()))

    def damage(self, the_damage: int) -> None:
        """
        This method allows the monster to take damage
        :param the_damage: The amount of damage to take
        :return: True if the monster is still alive, False otherwise
        """
        super().damage(the_damage)
        if self.is_alive():
            self.heal()
