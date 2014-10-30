import random
from util.vectorsprites import *
from shooter import *
from soundManager import *

# four different rock shapes
# can be small, medium, or large
# the smaller, the faster
class Rock(VectorSprite):

	# indexes into the tuples below
	large_rock = 0
	medium_rock = 1
	small_rock = 2

	velocities = (1.5, 4.0, 6.0)
	scales = (2.5, 1.5, 0.6)

	# tracks last rock to be made
	rock_shape = 1

	# create rock to given scale
	def __init__(self, stage, position, rock_type):

		scale = Rock.scales[rock_type]
		velocity = Rock.velocities[rock_type]
		heading = Vector2d(random.uniform(-velocity, velocity), random.uniform(-velocity, velocity))

		# ensure that rocks don't just sit there or move along regular lines
		if heading.x == 0:
			heading.x = 0.1

		if heading.y == 0:
			heading.y = 0.1

		self.rock_type = rock_type
		point_list = self.create_point_list()
		new_point_list = [self.scale(point, scale) for point in point_list]
		VectorSprite.__init__(self, position, heading, new_point_list)

	# create different rock type point_lists
	def create_point_list(self):

		if (Rock.rock_shape == 1):
			point_list = [(-4,-12), (6,-12), (13, -4), (13, 5), (6, 13), (0,13), (0,4),\
					(-8,13), (-15, 4), (-7,1), (-15,-3)]

		elif (Rock.rock_shape == 2):
			point_list = [(-6,-12), (1,-5), (8, -12), (15, -5), (12,0), (15,6), (5,13),\
						(-7,13), (-14,7), (-14,-5)]

		elif (Rock.rock_shape == 3):
			point_list = [(-7,-12), (1,-9), (8,-12), (15,-5), (8,-3), (15,4), (8,12),\
						(-3,10), (-6,12), (-14,7), (-10,0), (-14,-5)]            

		elif (Rock.rock_shape == 4):
			point_list = [(-7,-11), (3,-11), (13,-5), (13,-2), (2,2), (13,8), (6,14),\
						(2,10), (-7,14), (-15,5), (-15,-5), (-5,-5), (-7,-11)]

		Rock.rock_shape += 1
		if (Rock.rock_shape == 5):
			Rock.rock_shape = 1

		return point_list

	# spin rock when it moves
	def move(self):
		VectorSprite.move(self)

		self.angle += 1

class Debris(Point):

	def __init__(self, position, stage):
		heading = Vector2d(random.uniform(-15, 1.5), random.uniform(-1.5, 1.5))
		Point.__init__(self, position, heading, stage)
		self.ttl = 50

	def move(self):
		Point.move(self)
		r,g,b = self.color
		r -= 5
		g -= 5
		b -= 5
		self.color = (r, g, b)

# FLYING SAUCER OF DOOM
class Saucer(Shooter):

	# indexes into the tuples below
	large_saucer = 0
	small_saucer = 1

	velocities = (1.7, 3.0)
	scales = (1.5, 1.0)
	scores = (500, 1000)
	point_list = [(-9,0), (-3,-3), (-2,-6), (-2,-6), (2,-6), (3,-3), (9,0), (-9,0), (-3,4), (3,4), (9,0)]
	max_bullets = 1
	bullet_ttl = [60, 90]
	bullet_velocity = 5

	def __init__(self, stage, saucer_type, ship):
		position = Vector2d(0.0, random.randrange(0, stage.height))
		heading = Vector2d(self.velocities[saucer_type], 0.0)
		self.saucer_type = saucer_type
		self.ship = ship
		self.score_value = self.scores[saucer_type]
		stop_sound('ssaucer')
		stop_sound('lsaucer')
		if saucer_type == self.large_saucer:
			play_sound_continuous('lsaucer')
		else:
			play_sound_continuous('ssaucer')
		self.laps = 0
		self.last_x = 0

		# scale shape and create VectorSprite
		new_point_list = [self.scale(point, self.scales[saucer_type]) for point in self.point_list]
		Shooter.__init__(self, position, heading, new_point_list, stage)

	def move(self):
		Shooter.move(self)

		if (self.position.x > self.stage.width * 0.33) and (self.position.x < self.stage.width * 0.66):
			self.heading.y = self.heading.x
		else:
			self.heading.y = 0

		self.FIRE()

		# lapped map?
		if self.last_x > self.position.x:
			self.last_x = 0
			self.laps += 1
		else:
			self.last_x = self.position.x

	def FIRE(self):
		if self.ship is not None:
			dx = self.ship.position.x - self.position.x
			dy = self.ship.position.y - self.poitions.y
			mag = math.sqrt(dx*dx + dy*dy)
			heading = Vector2d(self.bullet_velocity * (dx/mag), self.bullet_velocity * (dy/mag))
			position = Vector2d(self.position.x, self.position.y)
			shot_fired = Shooter.FIRE(self, heading, self.bullet_ttl[self.saucer_type], self.bullet_velocity)
			if shot_fired:
				play_sound('saucer_fire')