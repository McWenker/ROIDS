import random
from util.vectorsprites import *
from util import *

class Shooter(VectorSprite):

	def __init__(self, position, heading, point_list, stage):
		VectorSprite.__init__(self, position, heading, point_list)
		self.bullets = []
		self.stage = stage

	def FIRE(self, heading, ttl, velocity):
		if (len(self.bullets) < self.max_bullets):
			position = Vector2d(self.position.x, self.position.y)
			new_bullet = Bullet(position, heading, self, ttl, velocity, self.stage)
			self.bullets.append(new_bullet)
			self.stage.add_sprite(new_bullet)
			return True

	def bullet_collision(self, target):
		collision_detected = False
		for bullet in self.bullets:
			if bullet.ttl > 0 and target.collidesWith(bullet):
				collision_detected = True
				bullet.ttl = 0

		return collision_detected

class Bullet(Point):

	def __init__(self, position, heading, shooter, ttl, velocity, stage):
		Point.__init__(self, position, heading, stage)
		self.shooter = shooter
		self.ttl = ttl
		self.velocity = velocity

	def move(self):
		Point.move(self)
		if (self.ttl <= 0):
			self.shooter.bullets.remove(self)