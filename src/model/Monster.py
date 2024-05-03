from src.model.DungeonCharacter import DungeonCharacter
from random import random
from abc import ABC
from src.controller.DatabaseController import DatabaseController as DB


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

    def __init__(self, the_name: str, the_class: str) -> None:
        """
        Constructor for the Monster class
        :param the_name: The name of the monster
        :param the_class: The class that instantiated the monster
        """
        super().__init__(the_name, Monster.__name__, the_class)
        # incorporate SQLite driver for this?
        data = DB().get_stats(Monster.__name__, the_class)
        self.__my_chance_to_heal = data['chance_to_heal']
        self.__my_min_heal = data['min_heal']
        self.__my_max_heal = data['max_heal']

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
            self.set_health(int(random() * (self.__my_max_heal - self.__my_min_heal) + self.__my_min_heal))

    def attack(self, other: DungeonCharacter) -> bool:
        """
        This method allows the monster to attack a hero
        :param other: The hero to attack
        :return: True if the attack was successful, False otherwise
        """
        if random() <= self.get_chance_to_hit():
            damage: int = int(random() * (self.get_damage_max() - self.get_damage_min()) + self.get_damage_min())
            return other.damage(damage)

    def damage(self, the_damage: int) -> bool:
        """
        This method allows the monster to take damage
        :param the_damage: The amount of damage to take
        :return: True if the monster is still alive, False otherwise
        """
        if not super().damage(the_damage):
            self.heal()
            return False
        return True
