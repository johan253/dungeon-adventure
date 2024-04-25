from random import random as random_float
from abc import ABC


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
        return cls.__new__(cls, *args, **kwargs)

    def __init__(self, the_name: str, the_class: type) -> None:
        """
        Constructor for the abstract DungeonCharacter class
        :param the_name: the name of the character
        :param the_class: the class that instantiated the character
        """
        self.__my_name = the_name
        self.__my_class = the_class
        # Set default values for the rest of the attributes, as sqlite3 database not yet implemented
        # TODO: Implement sqlite3 database to retrieve character attributes
        self.__my_health = 0
        self.__my_damage_min = 0
        self.__my_damage_max = 0
        self.__my_attack_speed = 0
        self.__my_chance_to_hit = 0.0

    def attack(self, the_other_character: 'DungeonCharacter') -> bool:
        """
        This method allows the character to attack another character
        :param the_other_character: the character to attack
        :return: True if the attack was successful, False otherwise
        """
        dice_roll: float = random_float()
        if dice_roll <= self.__my_chance_to_hit:
            damage: int = int(random_float() * (self.__my_damage_max - self.__my_damage_min) + self.__my_damage_min)
            the_other_character.set_health(the_other_character.get_health() - damage)
            return True
        else:
            return False

    def get_name(self) -> str:
        """
        Getter for the name of the character
        :return: the name of the character
        """
        return self.__my_name

    def get_class(self) -> type:
        """
        Getter for the class of the character
        :return: the class that instantiated the character
        """
        return self.__my_class

    def get_health(self) -> int:
        """
        Getter for the health of the character
        :return: the health of the character
        """
        return self.__my_health

    def set_health(self, health: int) -> None:
        """
        Setter for the health of the character
        :param health: the new health of the character
        """
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
                f" Health: {self.__my_health}"
                )
