from Monster import Monster


class Ogre(Monster):
    DEFAULT_NAME = "Ogre"

    def __init__(self, name=DEFAULT_NAME):
        super().__init__(name)
