import pygame, sys, os, random
from pygame.locals import *

sounds = {}

def init_sound_manager():
	pygame.mixer.init()
	sounds['fire'] = pygame.mixer.Sound('../res/laserfire02.ogg')
	sounds['explode1'] = pygame.mixer.Sound('../res/EXPLODE1.WAV')
	sounds["explode2"] = pygame.mixer.Sound("../res/EXPLODE2.WAV")
	sounds["explode3"] = pygame.mixer.Sound("../res/EXPLODE3.WAV")
	sounds["lsaucer"] = pygame.mixer.Sound("../res/LSAUCER.WAV")
	sounds["ssaucer"] = pygame.mixer.Sound("../res/SSAUCER.WAV")
	sounds["thrust"] = pygame.mixer.Sound("../res/THRUST.ogg")
	sounds["sfire"] = pygame.mixer.Sound("../res/SFIRE.WAV")
	sounds["extralife"] = pygame.mixer.Sound("../res/LIFE.WAV")

def play_sound(sound_name):
	channel = sounds[sound_name].play()

def play_sound_continuous(sound_name):
	channel = sounds[sound_name].play(-1)

def stop_sound(sound_name):
	channel = sounds[sound_name].stop()