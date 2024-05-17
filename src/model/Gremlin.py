from src.model.Monster import Monster


class Gremlin(Monster):
    """
    This class represents a Gremlin monster in the game
    Attributes:
        - DEFAULT_NAME: String
            The default name for the Gremlin monster
    """
    DEFAULT_NAME = "Gremlin"

    def __init__(self, the_name: str, the_health: int, the_min_damage: int, the_max_damage: int,
                 the_attack_speed: int, the_chance_to_hit: int, the_chance_to_heal: int,
                 the_min_heal: int, the_max_heal: int) -> None:
        """
        Constructor for the Gremlin class
        :param the_name: The name of the Gremlin
        :param the_health: The health of the Gremlin
        :param the_min_damage: The minimum damage the Gremlin can deal
        :param the_max_damage: The maximum damage the Gremlin can deal
        :param the_attack_speed: The attack speed of the Gremlin
        :param the_chance_to_hit: The chance to hit of the Gremlin
        :param the_chance_to_heal: The chance that the Gremlin will heal itself
        :param the_min_heal: The minimum amount that the Gremlin can heal
        :param the_max_heal: The maximum amount that the Gremlin can heal
        """
        super().__init__(the_name, the_health, the_min_damage, the_max_damage, the_attack_speed, the_chance_to_hit,
                         the_chance_to_heal, the_min_heal, the_max_heal)
