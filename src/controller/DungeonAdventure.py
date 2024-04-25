class DungeonAdventure:
    """
    This class represents the controller for the dungeon adventure game
    Attributes:
        - my_player: DungeonCharacter
        - my_inventory: List[DungeonItem]
        - my_dungeon: Dungeon
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        """
        This method is called before the __init__ method, and is overwritten
        to prevent more than once instance of this class from being created
        :param args: the arguments passed to the class constructor
        """
        if not hasattr(cls, '__instance'):
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance

    def run(self) -> None:
        """
        This method runs the dungeon adventure game
        """
        print("Welcome to Dungeon Adventure!")
        print("You are now in the dungeon. Good luck!")