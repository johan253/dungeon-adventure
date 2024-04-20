from Monster import Monster


class Gremlin(Monster):
    DEFAULT_NAME = "Gremlin"

    def __init__(self, name=DEFAULT_NAME):
        super().__init__(name)
