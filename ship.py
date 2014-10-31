import random
from util.vectorsprites import *
from shooter import *
from math import *
from soundManager import *

class Ship(Shooter):

	# attributes
	acceleration = 0.2
	deceleration = -0.005
	max_velocity = 10
	turn_angle = 6
	bullet_velocity = 13.0
	max_bullets = 4
	bullet_ttl = 35

	def __init__(self, stage):

		position = Vector2d(stage.width/2, stage.height/2)
		heading = Vector2d(0, 0)
		self.thrust_jet = Thruster(stage, self)
		self.ship_debris_list = []
		self.visible = True
		self.in_hyperspace = False
		point_list = [(0, -10), (6, 10), (3, 7), (-3, 7), (-6, 10)]

		Shooter.__init__(self, position, heading, point_list, stage)

	def draw(self):
		if self.visible:
			if not self.in_hyperspace:
				VectorSprite.draw(self)
			else:
				self.hyperspace_ttl -= 1
				if self.hyperspace_ttl == 0:
					self.in_hyperspace = False
					self.color (255, 255, 255)
					self.thrust_jet.color = (255, 255, 255)
					self.position.x = random.randrange(0, self.stage.width)
					self.position.y = random.randrange(0, self.stage.height)
					position = Vector2d(self.position.x, self.position.y)
					self.thrust_jet.position = position

		return self.transformedPointlist

	def rotate_left(self):
		self.angle += self.turn_angle
		self.thrust_jet.angle += self.turn_angle

	def rotate_right(self):
		self.angle -= self.turn_angle
		self.thrust_jet.angle -= self.turn_angle

	def thrust(self):
		play_sound_continuous('thrust')
		if math.hypot(self.heading.x, self.heading.y) > self.max_velocity:
			return

		dx = self.acceleration * math.sin(radians(self.angle)) * -1
		dy = self.acceleration * math.cos(radians(self.angle)) * -1
		self.change_velocity(dx, dy)

	def decrease_thrust(self):
		stop_sound('thrust')
		if (self.heading.x == 0 and self.heading.y == 0):
			return

		dx = self.heading.x * self.deceleration
		dy = self.heading.y * self.deceleration
		self.change_velocity(dx, dy)

	def change_velocity(self, dx, dy):
		self.heading.x += dx
		self.heading.y += dy
		self.thrust_jet.heading.x += dx
		self.thrust_jet.heading.y += dy

	def move(self):
		VectorSprite.move(self)
		self.decrease_thrust()

	# break the ship down into sadness and grief
	def explode(self):
		pointlist = [(0,-10),(6,10)]
		self.add_ship_debris(pointlist)        
		pointlist = [(6,10), (3,7)]
		self.add_ship_debris(pointlist)
		pointlist = [(3,7), (-3,7)]
		self.add_ship_debris(pointlist)
		pointlist = [(-3,7), (-6,10)]
		self.add_ship_debris(pointlist)
		pointlist = [(-6,10), (0,-10)]
		self.add_ship_debris(pointlist)

	# create piece of ship debris
	def add_ship_debris(self, point_list):
		heading = Vector2d(0, 0)
		position = Vector2d(self.position.x, self.position.y)
		debris = VectorSprite(position, heading, point_list, self.angle)

		# add debris to stage
		self.stage.add_sprite(debris)

		# calc velocity moving away from ship's center
		center_x = debris.boundingRect.centerx
		center_y = debris.boundingRect.centery

		# alter random values below to change rate of expansion
		debris.heading.x = ((center_x - self.position.x) + 0.1) / random.uniform(20, 40)
		debris.heading.y = ((center_y - self.position.y) + 0.1) / random.uniform(20, 40)
		self.ship_debris_list.append(debris)

	# set bullet velocity and create bullet
	def FIRE(self):
		if self.in_hyperspace == False:
			vx = self.bullet_velocity * math.sin(radians(self.angle)) * -1
			vy = self.bullet_velocity * math.cos(radians(self.angle)) * -1
			heading = Vector2d(vx, vy)
			Shooter.FIRE(self, heading, self.bullet_ttl, self.bullet_velocity)
			play_sound('fire')

	def enter_hyperspace(self):
		if not self.in_hyperspace:
			self.in_hyperspace = True
			self.hyperspace_ttl = 100
			self.color = (0, 0, 0)
			self.thrust_jet.color (0, 0, 0)

# exhaust when ship is accelerating
class Thruster(VectorSprite):
	point_list = [(-3, 7), (0, 13), (3, 7)]

	def __init__(self, stage, ship):
		position = Vector2d(stage.width/2, stage.height/2)
		heading = Vector2d(0, 0)
		self.accelerating = False
		self.ship = ship
		VectorSprite.__init__(self, position, heading, self.point_list)

	def draw(self):
		if self.accelerating and self.ship.in_hyperspace == False:
			self.color = (255, 255, 255)
		else:
			self.color = (0, 0, 0)

		VectorSprite.draw(self)
		return self.transformedPointlist