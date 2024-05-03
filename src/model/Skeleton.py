from src.model.Monster import Monster


class Skeleton(Monster):
    """
    This class represents a Skeleton monster in the game
    Attributes:
        - DEFAULT_NAME: String
            The default name for the Skeleton monster
    """
    DEFAULT_NAME = "Skeleton"

    def __init__(self, name=DEFAULT_NAME) -> None:
        """
        Constructor for the Skeleton class
        :param name: The name of the Skeleton
        """
        super().__init__(name, Skeleton.__name__)
