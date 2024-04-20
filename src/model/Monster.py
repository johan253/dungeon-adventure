from DungeonCharacter import DungeonCharacter
class Monster(DungeonCharacter):
    def __init__(self,my_name,my_class,my_chance_to_heal):
        super().__init__(my_name,my_class)
        self.my_chance_to_heal = my_chance_to_heal

    def get_chance_to_heal(self):
        return self.my_chance_to_heal
    def attack(self,other):
        pass
