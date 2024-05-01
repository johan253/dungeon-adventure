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

    def __init__(self, the_name, the_class) -> None:
        """
        Constructor for the Hero class
        :param the_name: The name of the hero
        :param the_class: The class that instantiated the hero
        """
        super().__init__(the_name, the_class)
        # use SQLite database to retrieve this value?
        self.__my_chance_to_block = 0.1

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

    def attack(self, other: DungeonCharacter) -> bool:
        """
        This method allows the hero to attack a monster
        :param other: The monster to attack
        :return: True if the attack was successful, False otherwise
        """
        if random() <= self.get_chance_to_hit():
            damage: int = int(random() * (self.get_damage_max() - self.get_damage_min()) + self.get_damage_min())
            return other.damage(damage)

    def damage(self, amount: int) -> bool:
        """
        This method damages the hero by a certain amount
        :param amount: The amount of damage to deal to the hero
        """
        if random() >= self.__my_chance_to_block:
            return super().damage(amount)
        return False
