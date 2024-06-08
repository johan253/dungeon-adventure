import pygame
from src.model import Warrior, Thief, Priestess, Ogre, Gremlin, Skeleton

WARRIOR = Warrior.Warrior.DEFAULT_NAME
THIEF = Thief.Thief.DEFAULT_NAME
PRIESTESS = Priestess.Priestess.DEFAULT_NAME
OGRE = Ogre.Ogre.DEFAULT_NAME
GREMLIN = Gremlin.Gremlin.DEFAULT_NAME
SKELETON = Skeleton.Skeleton.DEFAULT_NAME


def get_sprite(character: str) -> pygame.Surface:
    """
    This function gets the sprite for the current character.
    :param character: Current character being used in game data.
    :return:
    """
    image = pygame.image.load(f"Assets/{character}.png")
    image = pygame.transform.scale(image, (250, 250))
    return image


