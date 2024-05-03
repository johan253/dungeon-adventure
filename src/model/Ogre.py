from src.model.Monster import Monster


class Ogre(Monster):
    """
    This class represents an Ogre monster in the game
    Attributes:
        - DEFAULT_NAME: String
            The default name for the Ogre monster
    """
    DEFAULT_NAME = "Ogre"

    def __init__(self, name=DEFAULT_NAME) -> None:
        """
        Constructor for the Ogre class
        :param name: The name of the Ogre
        """
        super().__init__(name, Ogre.__name__)
