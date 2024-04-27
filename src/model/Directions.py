from enum import Enum


class Direction(Enum):
    """
    Enum for the different directions where there is a door in a room.
    """
    Direction = Enum('Direction', ['North', 'East', 'South', 'West'])
