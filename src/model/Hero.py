from DungeonCharacter import DungeonCharacter

class Hero(DungeonCharacter):
    def __init__self(self,my_name,my_class,my_chance_to_block):
        super().__init__(my_name,my_class)
        self.my_chance_to_block = my_chance_to_block

    def do_special(self,other):
        pass

    def get_chance_to_block(self):
        return self.my_chance_to_block

    def attack(self,other):
        pass


