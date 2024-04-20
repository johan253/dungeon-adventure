class DungeonCharacter:
    def __init__(self, my_name, my_class):
        self.__my_name = my_name # String
        self.__my_class = my_class # Class
        self.__my_health = 0 # Default health
        self.__my_damage_min = 0  # Default minimum damage
        self.__my_damage_max = 0  # Default maximum damage
        self.__my_attack_speed = 0  # Default attack speed
        self.__my_chance_to_hit = 0.0  # Default chance to hit

    def attack(self, other):
        # Implement attack logic here
        # For simplicity, let's just return True for now
        return True

    def get_name(self):
        return self.__my_name

    def get_class(self):
        return self.__my_class

    def get_health(self):
        return self.__my_health

    def set_health(self, health):
        self.__my_health = health

    def get_damage_min(self):
        return self.__my_damage_min

    def get_damage_max(self):
        return self.__my_damage_max

    def get_attack_speed(self):
        return self.__my_attack_speed

    def get_chance_to_hit(self):
        return self.__my_chance_to_hit
