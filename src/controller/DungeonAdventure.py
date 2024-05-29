import pygame
import src.controller.DungeonEvent as DungeonEvent
from random import random, choice
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
        dim = choice([4, 6, 8])
        self.__my_dungeon = Dungeon(6, 6)  # Dungeon
        self.__my_location = self.__my_dungeon.get_root()
        self.__my_visited_rooms = set()
        self.__my_visited_rooms.add(self.__my_location)
        self.__my_battle_state = False
        # current rooms
        # dungeon
        self.item_effects = {
            RoomItem.HealingPotion: self.use_healing_potion,
            RoomItem.VisionPotion: self.use_vision_potion,
            RoomItem.BombPotion: self.use_bomb_potion,
            RoomItem.SpeedPotion: self.use_speed_potion
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
            return False

        self.__my_location = next_room
        self.__my_visited_rooms.add(next_room)
        for item in next_room.get_items():
            if item.value not in RoomItem.get_static_items():
                self.__my_inventory.append(item)
                print(f"DA: Picked up {item}")
        next_room.set_items([])

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

    def use_item(self, item_type: RoomItem) -> bool:
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
            print(f"Used {item_type}")
            return True
        else:
            print(f"No effect defined for {item_type}")
            return False

    def use_healing_potion(self, player):
        heal_amount = 50
        new_health = min(player.get_health() + heal_amount, player.get_max_health())
        player.set_health(new_health)
        print(f"{player.get_name()} healed by {heal_amount}, current health: {new_health}.")

    def use_vision_potion(self, player):
        surrounding_rooms = self.get_adjacent_rooms()
        for room in surrounding_rooms:
            if room is not None:
                self.__my_visited_rooms.add(room)
        print(f"{player.get_name()} uses a vision potion, revealing secrets in the surrounding rooms.")

    def use_bomb_potion(self, player, current_room):
        damage = 30
        if hasattr(current_room, 'monsters'):
            for monster in current_room.monsters:
                monster.damage(damage)
                if not monster.is_alive():
                    print(f"The monster {monster.get_name()} has been defeated")
        print(f"{player.get_name()} uses a bomb potion, dealing {damage} damage to all enemies in the room.")

    def use_speed_potion(self, player):
        original_speed = player.get_attack_speed()
        new_speed = original_speed + 5
        player.__my_attack_speed = new_speed
        print(f"{player.get_name()}'s speed increased from {original_speed} to {new_speed}.")

    def handle_event(self, event):
        """
        This method handles the events in the game.
        :param event: The event to be handled
        """
        if self.__my_battle_state:
            if event == DungeonEvent.BATTLE_ATTACK:
                fast_attacker = self.__my_player
                slow_attacker = self.__my_location.get_monster()
                if self.__my_player.get_attack_speed() < self.__my_location.get_monster().get_attack_speed():
                    fast_attacker = self.__my_location.get_monster()
                    slow_attacker = self.__my_player
                attack_ratio = fast_attacker.get_attack_speed() // slow_attacker.get_attack_speed()
                for _ in range(attack_ratio):
                    fast_attacker.attack(slow_attacker)
                if slow_attacker.is_alive():
                    slow_attacker.attack(fast_attacker)
                if not fast_attacker.is_alive() or not slow_attacker.is_alive():
                    self.__my_battle_state = False

            elif event == DungeonEvent.BATTLE_SPECIAL:
                print("Special Attack!")
            elif event == DungeonEvent.BATTLE_HEAL:
                print("Use Heal!")
        else:
            if event == DungeonEvent.GAMEPLAY_MOVE_NORTH:
                self.move_player('north')
            elif event == DungeonEvent.GAMEPLAY_MOVE_SOUTH:
                self.move_player('south')
            elif event == DungeonEvent.GAMEPLAY_MOVE_WEST:
                self.move_player('west')
            elif event == DungeonEvent.GAMEPLAY_MOVE_EAST:
                self.move_player('east')

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

    def get_current_room_coordinates(self) -> tuple[int, int]:
        for x in range(self.__my_dungeon.get_dimensions()[0]):
            for y in range(self.__my_dungeon.get_dimensions()[1]):
                if self.__my_dungeon.get_room(x, y) == self.__my_location:
                    return x, y
        raise ValueError("Current room coordinates not found.")

    def get_adjacent_rooms(self) -> list[DungeonRoom]:
        """
        This method returns a list of adjacent rooms to the current room
        :return: List of adjacent rooms
        """
        x, y = self.get_current_room_coordinates()
        adjacent_rooms = [
            self.__my_dungeon.get_room(x - 1, y),  # West
            self.__my_dungeon_get_room(x + 1, y),  # East
            self.__my_dungeon.get_room(x, y - 1),  #North
            self.__my_dungeon.get_room(x, y + 1)  # South
        ]
        return adjacent_rooms

    def get_game_data(self):
        """
        This method returns the state of current game.
        :return: The state of the game
        """
        return [self.__my_player, self.__my_inventory, self.__my_dungeon]
