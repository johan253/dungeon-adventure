from model.Monster import Monster


class Skeleton(Monster):
    """
    This class represents a Skeleton monster in the game
    Attributes:
        - DEFAULT_NAME: String
            The default name for the Skeleton monster
    """
    DEFAULT_NAME = "Skeleton"

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_heal: int,
                 the_min_heal: int, the_max_heal: int) -> None:
        """
        Constructor for the Skeleton class
        :param the_name: The name of the Skeleton
        :param the_health: The health of the Skeleton
        :param the_min_damage: The minimum damage the Skeleton can deal
        :param the_max_damage: The maximum damage the Skeleton can deal
        :param the_attack_speed: The attack speed of the Skeleton
        :param the_chance_to_hit: The chance to hit of the Skeleton
        :param the_chance_to_heal: The chance that the Skeleton will heal itself
        :param the_min_heal: The minimum amount that the Skeleton can heal
        :param the_max_heal: The maximum amount that the Skeleton can heal
        """
        if not any([the_health, the_min_damage, the_max_damage, the_attack_speed,
                    the_chance_to_hit, the_chance_to_heal, the_min_heal, the_max_heal]):
            raise ValueError("All parameters must be provided to create a Skeleton")
        if the_name.strip() == "":
            the_name = self.DEFAULT_NAME
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                         the_chance_to_heal, the_min_heal, the_max_heal)
