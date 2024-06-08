from src.model.DungeonCharacter import DungeonCharacter
from random import random
from abc import ABC, abstractmethod


class Hero(DungeonCharacter, ABC):
    """
    This class represents a hero (user) in the Dungeon Adventure game
    Attributes:
        - my_chance_to_block: Float
            The chance that the hero will block an attack
    """
    def __new__(cls, *args, **kwargs):
        """
        This method overrides the __new__ method to prevent instantiation of the abstract Hero class
        :param args: The arguments to pass to the constructor
        :param kwargs: The keyword arguments to pass to the constructor
        :return: The new instance of the Hero class
        """
        if cls is Hero:
            raise TypeError("The Hero class may not be instantiated directly")
        return super().__new__(cls)

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_block: int) -> None:
        """
        Constructor for the Hero class
        :param the_name: The name of the hero
        :param the_health: The health of the hero
        :param the_min_damage: The minimum damage the hero can deal
        :param the_max_damage: The maximum damage the hero can deal
        :param the_attack_speed: The attack speed of the hero
        :param the_chance_to_hit: The chance to hit of the hero
        :param the_chance_to_block: The chance that the hero will block an attack
        """
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit)
        self.__my_chance_to_block: float = the_chance_to_block

    @abstractmethod
    def do_special(self, other: DungeonCharacter) -> bool:
        """
        This method allows the hero to perform a special attack or ability
        :param other: The monster to perform the special ability on
        :return: True if the special ability was successful, False otherwise
        """
        pass

    def get_chance_to_block(self) -> float:
        """
        This method returns the chance that the hero will block an attack
        :return: The chance that the hero will block an attack
        """
        return self.__my_chance_to_block

    def damage(self, amount: int) -> None:
        """
        This method damages the hero by a certain amount
        :param amount: The amount of damage to deal to the hero
        """
        if random() >= self.__my_chance_to_block:
            super().damage(amount)
