import pygame, sys, os
from pygame.locals import *

class Stage:

	# setup pygame surface
	def __init__(self, caption, dimensions=None):
		pygame.init()

		# if no screen size provided, pick first available
		if dimensions == None:
			dimensions = pygame.display.list_modes()[0]

		pygame.display.set_mode(dimensions, FULLSCREEN)
		pygame.mouse.set_visible(False)

		pygame.display.set_caption(caption)

		self.screen = pygame.display.get_surface()
		self.sprite_list = []
		self.width = dimensions[0]
		self.height = dimensions[1]
		self.show_bounding_boxes = False

	# adds sprite to list then draw it
	def add_sprite(self, sprite):
		self.sprite_list.append(sprite)
		sprite.boundingRect = pygame.draw.aalines(self.screen, sprite.color, True, sprite.draw())

	def remove_sprite(self, sprite):
		self.sprite_list.remove(sprite)

	def draw_sprites(self):
		for sprite in self.sprite_list:
			sprite.boundingRect = pygame.draw.aalines(self.screen, sprite.color, True, sprite.draw())
			if self.show_bounding_boxes == True:
				pygame.draw.rect(self.screen, (255, 255, 255), sprite.boundingRect, 1)

	def move_sprites(self):
		for sprite in self.sprite_list:
			sprite.move()

			if sprite.position.x < 0:
				sprite.position.x = self.width

			if sprite.position.x > self.width:
				sprite.position.x = 0

			if sprite.position.y < 0:
				sprite.position.y = self.height

			if sprite.position.y > self.height:
				sprite.position.y = 0