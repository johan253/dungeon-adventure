from Monster import Monster


class Skeleton(Monster):
    DEFAULT_NAME = "Skeleton"

    def __init__(self, name=DEFAULT_NAME):
        super().__init__(name)
