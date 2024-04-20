class DatabaseDriver:
    """
    A Singleton class used to communicate with the database

    Attributes:
        _instance: An instance of the DatabaseDriver class

    Methods:
        get_stats(): Gets the stats of the given DungeonCharacter class
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Overridden __new__ method to create an instance of the DatabaseDriver class
        using the Singleton Design pattern
        :param args:
        :param kwargs:
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def get_stats(self, dungeon_character: type):
        pass
