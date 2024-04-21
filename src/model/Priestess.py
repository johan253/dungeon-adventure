from DungeonCharacter import DungeonCharacter


class Thief(DungeonCharacter):
    DEFAULT_NAME = "Priestess"

    def __init__(self, my_name=DEFAULT_NAME, my_class=None, my_chance_to_block=0.0):
        super().__init__(my_name, my_class, my_chance_to_block)

    def do_special(self, other):
        pass
