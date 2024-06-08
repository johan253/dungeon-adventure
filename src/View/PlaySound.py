import pygame


def music(sound_file, loop):
    """
    This fucntion plays the music for the background.
    :param sound_file: The file path to the music
    :param loop: An int representing the amount of loop that will occur.
    :return:
    """
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(loops=loop)


def sound_efx(music_file, loop):
    """
    This fucntion will play the sound effect for the dungeon.
    :param music_file: The file path to the sound effect.
    :param loop: An int representing the amount of loop that will occur.
    :return:
    """
    efx = pygame.mixer.Sound(music_file)
    efx.play(loops=loop)