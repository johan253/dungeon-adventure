import pygame


def music(sound_file, loop):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play(loops=loop)


def sound_efx(music_file, loop):
    efx = pygame.mixer.Sound(music_file)
    efx.play(loops=loop)