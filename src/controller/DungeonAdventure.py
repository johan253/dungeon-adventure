from random import random

from model.DugeonRoom import DungeonRoom
from model.DungeonCharacter import DungeonCharacter
from model.Dungeon import Dungeon
from model.CharacterFactory import CharacterFactory
from model.RoomItem import RoomItem


class DungeonAdventure:
    """
    This class is the controller for the Dungeon Adventure game. It is responsible for managing the player, the dungeon,
    and the inventory. It also handles the movement of the player and the use of items.
    Attributes:
        - __my_player (Player): The player object
        - __my_inventory (List[RoomItem]): The inventory of the player
        - __my_dungeon (Dungeon): The dungeon object
    """

    def __init__(self, player_name: str, player_class: str):
        """
        This method initializes the Dungeon Adventure game.
        :param player_name: The name of the player
        :param player_class: The class of the player
        """
        print("DA: Initializing Game...")
        self.__my_player = CharacterFactory().create_character(player_class, player_name)
        print("DA: \n", self.__my_player)
        self.__my_inventory: list[RoomItem] = []  # RoomItem
        self.__my_dungeon = Dungeon(5, 5)  # Dungeon
        self.__my_location = self.__my_dungeon.get_root()
        self.__my_visited_rooms = set()
        self.__my_visited_rooms.add(self.__my_location)
        self.__my_battle_state = False
        # currrent rooms
        # dungeon
        self.item_effects = {
            RoomItem.HealingPotion: lambda player: self.use_healing_potion(player),
            RoomItem.VisionPotion: lambda player, room: self.use_vision_potion(player, room),
            RoomItem.BombPotion: lambda player, room: self.use_bomb_potion(player, room),
            RoomItem.SpeedPotion: lambda player: self.use_speed_potion(player)
        }

    def move_player(self, direction) -> bool:
        """
            This method moves the player in the specified direction.
            :param direction: The direction to move ('north', 'south', 'east', 'west')
            :return: True if the move was successful and False otherwise.
        """
        current_room = self.__my_location
        next_room: DungeonRoom = getattr(current_room, f'get_{direction}')()

        if next_room is None:
            print(f"DA: No room with {direction}")
            return False

        self.__my_location = next_room
        self.__my_visited_rooms.add(next_room)
        for item in next_room.get_items():
            if item.value not in RoomItem.get_static_items():
                self.__my_inventory.append(item)
                print(f"DA: Picked up {item}")
        next_room.set_items([])
        print(f"Moved {direction} to a new room.")

        monster = next_room.get_monster()
        if monster:
            # TODO: Implement battle somehow? Gameplay.py currently just uses this state to swap to battle screen.
            self.__my_battle_state = True
        return True

    def get_battle_state(self):
        """
        This method returns the battle state of the game.
        :return: The battle state of the game
        """
        return self.__my_battle_state

    def use_item(self, item_type: RoomItem) -> bool:  # item = Room-Item
        """
        This method uses the specified item.
        :param item_type: Room item to be used
        :return: True if the item was used successfully, False otherwise
        """
        # Find item in inventory

        item = next((item for item in self.__my_inventory if item == item_type), None)
        if not item:
            print(f"Item {item_type} not found in inventory")
            return False

        # call the effect if the item exists within the map

        effect_function = self.item_effects.get(item_type)
        if effect_function:
            effect_function(self.__my_player)
            self.__my_inventory.remove(item)
            print("fUsed {item_type}")
            return True
        else:
            print(f"No effect defined for {item_type}")
            return False

    def use_healing_potion(self,player):
        heal_amount = 50
        new_health = min(player.get_health() + heal_amount, player.get_max_health())
        player.set_health(new_health)
        print(f"{player.get_name()} healed by {heal_amount}, current health: {new_health}.")

    def use_vision_potion(self, player, current_room):
        # This is a placeholder
        print(f"{player.get_name()} uses a vision potion, revealing secrets in the room.")

    def use_bomb_potion(self,player,current_room):
        damage = 30
        if hasattr(current_room,'monsters'):
            for monster in current_room.monsters:
                monster.damage(damage)
                if not monster.is_alive():
                    print(f"The monster {monster.get_name()} has been defeated")
        print(f"{player.get_name()} uses a bomb potion, dealing {damage} damage to all enemies in the room.")

    def use_speed_potion(self,player):
        original_speed = player.get_attack_speed()
        new_speed = original_speed + 5
        player.__my_attack_speed = new_speed
        print(f"{player.get_name()}'s speed increased from {original_speed} to {new_speed}.")

    def __battle(self, player, monster):
        """
        This method handles a battle between the player and a monster.
        :param player: The player character
        :param monster: The monster character
        :return: True if the player wins or escapes, False if the player is defeated.
        """
        if monster is None:
            print("No monster to fight.")
            return True

        print(f"You have encountered a {monster.get_name()}! Prepare for battle.")
        while player.get_health() > 0 and monster.get_health() > 0:
            print(
                f"\n{player.get_name()} Health: {player.get_health()} | {monster.get_name()} Health: {monster.get_health()}")
            print("Choose your action:")
            print("1. Attack")
            print("2. Use Special Ability")
            print("3. Attempt to flee")

            battle_choice = input("Enter the number of the action you want to take: ")
            while battle_choice not in ["1", "2"]:
                print("Invalid input. Please enter 1 to attack or 2 to flee.")
                battle_choice = input("Enter the number of the action you want to take: ")

            if battle_choice == "1":
                print(f"\n{player.get_name()} attacks {monster.get_name()}!")
                prev_health = monster.get_health()
                if player.attack(monster):
                    damage = prev_health - player.get_health()
                    print(f"Successful hit! {monster.get_name()} takes {damage} damage.")
                else:
                    print(f"{player.get_name()} missed the attack!")

                if monster.get_health() > 0:
                    print(f"\n{monster.get_name()} counterattacks!")
                    prev_health = player.get_health()
                    if monster.attack(player):
                        damage = prev_health - player.get_health()
                        print(f"Monster hits! {player.get_name()} takes {damage} damage.")
                    else:
                        print(f"{monster.get_name()} missed the attack!")
            elif battle_choice == "3":
                if random() < 0.5:
                    print("Successfully fled the battle!")
                    return True
                else:
                    print("Failed to flee! The battle continues.")
                    if monster.attack(player):
                        damage = monster.get_damage_max() - monster.get_damage_min()
                        print(f"Monster hits during your attempt to flee! {player.get_name()} takes {damage} damage.")
            elif battle_choice == "2":
                print(f"\n{player.get_name()} uses a special ability!")
                prev_health = monster.get_health()
                if player.do_special(monster):
                    damage = prev_health - monster.get_health()
                    print(f"Successful special ability! {monster.get_name()} takes {damage} damage.")
                else:
                    print(f"{player.get_name()}'s special ability failed!")
                if monster.is_alive():
                    print(f"\n{monster.get_name()} counterattacks!")
                    if monster.attack(player):
                        damage = monster.get_damage_max() - monster.get_damage_min()
                        print(f"Monster hits! {player.get_name()} takes {damage} damage.")
                    else:
                        print(f"{monster.get_name()} missed the attack!")

        if player.get_health() <= 0:
            print(f"\n{player.get_name()} has been defeated by {monster.get_name()}!")
            return False
        else:
            print(f"\n{monster.get_name()} has been defeated!")
            return True

    def get_dungeon(self):
        """
        This method returns the dungeon object.
        :return: The dungeon object
        """
        return self.__my_dungeon

    def get_player(self):
        """
        This method returns the player object.
        :return: The player object
        """
        return self.__my_player

    def get_current_room(self):
        """
        This method returns the current room of the player.
        :return: The current room of the player
        """
        return self.__my_location

    def get_visited_rooms(self):
        """
        This method returns the rooms that have been visited by the player.
        :return: The rooms that have been visited by the player
        """
        return self.__my_visited_rooms

    def get_inventory(self):
        """
        This method returns the inventory of the player.
        :return: The inventory of the player
        """
        return self.__my_inventory

    def get_game_data(self):
        """
        This method returns the state of current game.
        :return: The state of the game
        """
        return [self.__my_player, self.__my_inventory, self.__my_dungeon]
