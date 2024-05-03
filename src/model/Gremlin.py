from src.model.Monster import Monster


class Gremlin(Monster):
    """
    This class represents a Gremlin monster in the game
    Attributes:
        - DEFAULT_NAME: String
            The default name for the Gremlin monster
    """
    DEFAULT_NAME = "Gremlin"

    def __init__(self, name=DEFAULT_NAME) -> None:
        """
        Constructor for the Gremlin class
        :param name: The name of the Gremlin
        """
        super().__init__(name, Gremlin.__name__)
