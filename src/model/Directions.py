from enum import Enum


class Direction(Enum):
    """
    Enum for the different directions where there is a door in a room.
    Attributes:
        - North: int
            Represents the direction north
        - East: int
            Represents the direction east
        - South: int
            Represents the direction south
        - West: int
            Represents the direction west
    """
    North = 1
    East = 2
    South = 3
    West = 4

    @classmethod
    def list(cls) -> [int]:
        """
        Returns a list of the values of the Direction enum
        :return: a list of the values of the Direction enum
        """
        return list(map(lambda c: c.value, Direction))
