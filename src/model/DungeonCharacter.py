from abc import ABC, abstractmethod
from random import random


class DungeonCharacter(ABC):
    """
    This class represents a generic dungeon character in Dungeon Adventure
    Attributes:
        - my_name: String
            Represents the name of the character
        - my_class: Class
            Represents the class that instantiated the character
        - my_health: Integer
            Represents the health of the character
        - my_damage_min: Integer
            The minimum damage the character can deal
        - my_damage_max: Integer
            The maximum damage the character can deal
        - my_attack_speed: Integer
            The attack speed of the character
        - my_chance_to_hit: Float
            The chance to hit of the character, expressed as a float between 0 and 1
    """

    def __new__(cls, *args, **kwargs) -> 'DungeonCharacter':
        """
        This method is called before the __init__ method, and is overwritten
        to prevent instantiation of the abstract class
        :param args: the arguments passed to the class constructor
        :param kwargs: the keyword arguments passed to the class constructor
        """
        if cls is DungeonCharacter:
            # Raise an error if the class is this abstract class
            raise TypeError("DungeonCharacter class is abstract and cannot be instantiated directly")
        return super().__new__(cls)

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int) -> None:
        """
        Constructor for the abstract DungeonCharacter class
        :param the_name: the name of the character
        :param the_health: the health of the character
        :param the_min_damage: the minimum damage the character can deal
        :param the_max_damage: the maximum damage the character can deal
        :param the_attack_speed: the attack speed of the character
        :param the_chance_to_hit: the chance to hit of the character
        """
        self.__my_name = the_name
        self.__my_health = the_health
        self.__my_max_health = the_health
        self.__my_damage_min = the_min_damage
        self.__my_damage_max = the_max_damage
        self.__my_attack_speed = the_attack_speed
        self.__my_chance_to_hit = the_chance_to_hit

    def attack(self, the_other_character: 'DungeonCharacter') -> bool:
        """
        This method allows the character to attack another character
        :param the_other_character: the character to attack
        :return: True if the attack was successful, False otherwise
        """
        if random() <= self.get_chance_to_hit():
            damage: int = int(random() * (self.get_damage_max() - self.get_damage_min()) + self.get_damage_min())
            the_other_character.damage(damage)
            return True
        return False

    def damage(self, damage: int) -> None:
        """
        This method damages the character by a certain amount
        :param damage: The amount of damage to deal to the character
        :return: True if the character is dead, False otherwise
        """
        if damage < 0:
            raise ValueError("Damage cannot be negative")
        self.__my_health -= damage
        self.__my_health = max(0, self.__my_health)

    def get_name(self) -> str:
        """
        Getter for the name of the character
        :return: the name of the character
        """
        return self.__my_name

    def get_health(self) -> int:
        """
        Getter for the health of the character
        :return: the health of the character
        """
        return self.__my_health

    def get_max_health(self) -> int:
        """
        Getter for the maximum health of the character
        :return: the maximum health of the character
        """
        return self.__my_max_health

    def is_alive(self) -> bool:
        """
        This method checks if the character is alive
        :return: True if the character is alive, False otherwise
        """
        return self.__my_health > 0

    def set_health(self, health: int) -> None:
        """
        Setter for the health of the character
        :param health: the new health of the character
        """
        if health < 0 or health > self.__my_max_health:
            raise ValueError("Health must be between 0 and the max health")
        self.__my_health = health

    def get_damage_min(self) -> int:
        """
        Getter for the minimum damage the character can deal
        :return: the minimum damage the character can deal
        """
        return self.__my_damage_min

    def get_damage_max(self) -> int:
        """
        Getter for the maximum damage the character can deal
        :return: the maximum damage the character can deal
        """
        return self.__my_damage_max

    def get_attack_speed(self) -> int:
        """
        Getter for the attack speed of the character
        :return: the attack speed of the character
        """
        return self.__my_attack_speed

    def get_chance_to_hit(self) -> float:
        """
        Getter for the chance to hit of the character
        :return: the chance to hit of the character
        """
        return self.__my_chance_to_hit

    def __str__(self) -> str:
        """
        String representation of the character
        :return: the string representation of the character
        """
        return (
                f"Name: {self.__my_name}"
                f"\nHealth: {self.__my_health}"
                f"\nType: {type(self).__name__}"
                )
