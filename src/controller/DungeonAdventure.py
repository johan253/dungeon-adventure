import pygame
import src.controller.DungeonEvent as DungeonEvent
from random import random, choice, randint
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
        - __my_location (DungeonRoom): The current location of the player
        - __my_visited_rooms (Set[DungeonRoom]): The rooms that have been visited by the player
        - __my_battle_state (bool): The battle state of the game, True if there is a battle, False otherwise
    """
    EASY = 6
    MEDIUM = 7
    HARD = 8

    def __init__(self, player_name: str, player_class: str, difficulty: int = EASY):
        """
        This method initializes the Dungeon Adventure game.
        :param player_name: The name of the player
        :param player_class: The class of the player
        """
        print("DA: Initializing Game...")
        self.__my_player = CharacterFactory().create_character(player_class, player_name)
        print("DA: \n", self.__my_player)
        self.__my_inventory: list[RoomItem] = []  # RoomItem
        self.__my_dungeon = Dungeon(difficulty, difficulty)  # Dungeon
        self.__my_location = self.__my_dungeon.get_root()
        self.__my_visited_rooms = set()
        self.__my_visited_rooms.add(self.__my_location)
        self.__my_battle_state = False
        # current rooms
        # dungeon

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
                self.__my_inventory.append(item.value)
                print(f"DA: Picked up {item}")
            if item.value == RoomItem.Pit.value:
                self.__my_player.damage(randint(1, 20))
                print(f"DA: Player fell into a pit and took 5 damage")
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"key": DungeonEvent.GAMEPLAY_PIT_DAMAGE}))
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
        item = next((item for item in self.__my_inventory if item == item_type.value), None)
        if not item:
            print(f"Item {item_type} not found in inventory")
            return False
        self.__my_inventory.remove(item)
        if item_type == RoomItem.HealingPotion:
            self.use_healing_potion(self.__my_player)
        elif item_type == RoomItem.VisionPotion:
            self.use_vision_potion(self.__my_player)
        return True

    def use_healing_potion(self, player: DungeonCharacter):
        if self.__my_player.get_health() == self.__my_player.get_max_health():
            return
        heal_amount = int(5 + random() * 10)
        new_health = min(player.get_health() + heal_amount, player.get_max_health())
        player.set_health(new_health)
        return

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
        # If there is a battle, handle the battle event
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
                player = self.__my_player
                monster = self.__my_location.get_monster()
                player.do_special(monster)
                if monster.is_alive():
                    monster.attack(player)
                if not player.is_alive() or not monster.is_alive():
                    self.__my_battle_state = False
            elif event == DungeonEvent.BATTLE_HEAL:
                self.use_healing_potion(self.__my_player)
        # If there is no battle, handle the gameplay event
        else:
            if event == DungeonEvent.GAMEPLAY_MOVE_NORTH:
                self.move_player('north')
            elif event == DungeonEvent.GAMEPLAY_MOVE_SOUTH:
                self.move_player('south')
            elif event == DungeonEvent.GAMEPLAY_MOVE_WEST:
                self.move_player('west')
            elif event == DungeonEvent.GAMEPLAY_MOVE_EAST:
                self.move_player('east')
            elif event == DungeonEvent.GAMEPLAY_GOD_MODE:
                for x in range(self.__my_dungeon.get_dimensions()[0]):
                    for y in range(self.__my_dungeon.get_dimensions()[1]):
                        self.__my_visited_rooms.add(self.__my_dungeon.get_room(x, y))
                self.__my_player._DungeonCharacter__my_max_health = 999999
                self.__my_player._DungeonCharacter__my_health = 999999
                self.__my_player._DungeonCharacter__my_damage_min = 999999
                self.__my_player._DungeonCharacter__my_damage_max = 999999
                self.__my_player._DungeonCharacter__my_chance_to_hit = 999999
            elif event == DungeonEvent.GAMEPLAY_USE_HEALING_POTION:
                if self.use_item(RoomItem.HealingPotion):
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"key": DungeonEvent.GAMEPLAY_USE_HEALING_POTION}))
            elif event == DungeonEvent.GAMEPLAY_USE_VISION_POTION:
                if self.use_item(RoomItem.VisionPotion):
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"key": DungeonEvent.GAMEPLAY_USE_VISION_POTION}))

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
        adjacent_rooms: list[DungeonRoom] = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.__my_dungeon.get_dimensions()[0] and 0 <= new_y < self.__my_dungeon.get_dimensions()[1]:
                adjacent_rooms.append(self.__my_dungeon.get_room(new_x, new_y))
        return adjacent_rooms

    def get_game_data(self):
        """
        This method returns the state of current game.
        :return: The state of the game
        """
        return [self.__my_player, self.__my_inventory, self.__my_dungeon]
