import pygame, sys, os, random
from pygame.locals import *
from util.vectorsprites import *
from ship import *
from stage import *
from baddies import *
from shooter import *
from soundManager import *

class Asteroids():

	exploding = 180

	def __init__(self):
		self.stage = Stage('ROIDS')
		self.paused = False
		self.frame_advance = False
		self.game_state = 'attract_mode'
		self.rocks = []
		self.create_rocks(3)
		self.saucer = None
		self.time = 1
		self.score = 0
		self.ship = None
		self.lives = 0

	def init_game(self):
		self.game_state = 'playing'
		[self.stage.remove_sprite(sprite) for sprite in self.rocks]
		if self.saucer is not None:
			self.kill_saucer()
		self.start_lives = 3
		self.create_ship()
		self.lives_list()
		self.score = 0
		self.rock = []
		self.num_rocks = 3
		self.next_life = 10000

		self.create_rocks(self.num_rocks)
		self.time = 1

	def create_ship(self):
		if self.ship:
			[self.stage.sprite_list.remove(debris) for debris in self.ship.ship_debris_list]
		self.ship = Ship(self.stage)
		self.stage.add_sprite(self.ship.thrust_jet)
		self.stage.add_sprite(self.ship)

	def lives_list(self):
		self.lives += 1
		self.lives_list = []
		for i in xrange(1, self.start_lives):
			self.add_life(i)

	def add_life(self, lifenumber):
		self.lives += 1
		ship = Ship(self.stage)
		self.stage.add_sprite(ship)
		ship.position.x = self.stage.width - (lifenumber * ship.BoundingRect.width) - 10
		ship.position.y = 0 + ship.BoundingRect.height
		self.lives_list.append(ship)

	def create_rocks(self, num_rocks):
		for _ in xrange(0, num_rocks):
			position = Vector2d(random.randrange(-10, 10), random.randrange(-10, 10))

			new_rock = Rock(self.stage, position, Rock.large_rock)
			self.stage.add_sprite(new_rock)
			self.rocks.append(new_rock)

	def play_game(self):

		clock = pygame.time.Clock()

		frame_count = 0.0
		time_passed = 0.0
		self.fps = 0.0

		## MAIN GAME LOOP ##
		while True:

			# fps
			time_passed += clock.tick(60)
			frame_count += 1
			if frame_count % 10 == 0:
				self.fps = (frame_count / (time_passed / 1000.0))
				time_passed = 0
				frame_count = 0

			self.time += 1

			self.input(pygame.event.get())

			if self.paused and not self.frame_advance:
				continue

			self.stage.screen.fill((0, 0, 0))
			self.stage.move_sprites()
			self.stage.draw_sprites()
			self.saucer_find()
			self.display_score()
			self.check_score()

			# event handler
			if self.game_state == 'playing':
				self.playing()
			elif self.game_state == 'exploding':
				self.exploding()
			else:
				self.display_text()

			# buffer draw
			pygame.display.flip()

	def playing(self):
		if self.lives == 0:
			self.game_state = 'attract_mode'
		else:
			self.process_keys()
			self.collisions()
			if len(self.rocks) == 0:
				self.level_up()

	def saucer_find(self):
		if self.saucer is not None:
			if self.saucer.laps >= 2:
				self.kill_saucer()

		# create saucer
		if self.time % 2000 == 0 and self.saucer is None:
			rand_val = random.randrange(0, 10)
			if rand_val <= 3:
				self.saucer = Saucer(self.stage, Saucer.small_saucer, self.ship)
			else:
				self.saucer = Saucer(self.stage, Saucer.large_saucer, self.ship)
			self.stage.add_sprite(self.saucer)

	def exploding(self):
		self.exploding_count += 1
		if self.exploding_count > self.exploding:
			self.game_state = 'playing'
			[self.stage.sprite_list.remove(debris) for debris in self.ship.ship_debris_list]
			self.ship.ship_debris_list = []

			if self.lives == 0:
				self.ship.visible = False
			else:
				self.create_ship()

	def level_up(self):
		self.num_rocks += 1
		self.create_rocks(self.num_rocks)

	# move this sometime
	def display_text(self):
		font1 = pygame.font.Font(None, 50)
		title = font1.render('ROIDS', True, (255, 255, 255))
		title_rect = title.get_rect(centerx=self.stage.width/2)
		title_rect.y = self.stage.height/2 - title_rect.height*2
		self.stage.screen.blit(title, title_rect)

		font2 = pygame.font.Font(None, 30)
		keys = font2.render('WASD: move, SPACE: fire, E: hyperspace, ESC: quit', True, (255, 255, 255))
		keys_rect = keys.get_rect(centerx=self.stage.width/2)
		keys_rect.y = self.stage.height/2 - keys_rect.height/2
		self.stage.screen.blit(keys, keys_rect)

		instruction = font1.render('Press ENT to play!', True, (255, 255, 255))
		instruction_rect = instruction.get_rect(centerx=self.stage.width/2)
		instruction_rect.y = self.stage.height/2 + instruction_rect.height
		self.stage.screen.blit(instruction, instruction_rect)

	def display_score(self):
		font2 = pygame.font.Font(None, 30)
		score_str = str('%06d' % self.score)
		score = font2.render(score_str, True, (255, 255, 255))
		score_rect = score.get_rect(centerx=40, centery=15)
		self.stage.screen.blit(score, score_rect)

	# should move this into Ship class at some point
	def input(self, events):
		self.frame_advance = False
		for event in events:
			if event.type == QUIT:
				self.terminate()
			elif event.type == KEYDOWN:
				if event.key == K_ESCAPE:
					self.terminate()
				if self.game_state == 'playing':
					if event.key == K_SPACE:
						self.ship.FIRE()
					elif event.key == K_e:
						self.ship.hyperspace()
				elif self.game_state == 'attract_mode':
					# start new game
					if event.key == K_RETURN:
						self.init_game()

				# needs pause function to actually accomplish anything
				if event.key == K_p:
					if self.paused:
						self.paused = False
					else:
						self.paused = True

				if event.key == K_f:
					pygame.display.toggle_fullscreen()

			elif event.type == KEYUP:
				if event.key == K_o:
					self.frameAdvance = True

	def process_keys(self):
		key = pygame.key.get_pressed()

		if key[K_LEFT] or key[K_a]:
			self.ship.rotate_left()
		elif key[K_RIGHT] or key[K_x]:
			self.ship.rotate_right()

		if key[K_UP] or key[K_w]:
			self.ship.thrust()
			self.ship.thrust_jet.accelerating = True
		else:
			self.ship.thrust_jet.accelerating = False

		if key[K_DOWN] or key[K_s]:
			self.ship.decel()
			self.ship.thrust_jet.accelerating = True
		else:
			self.ship.thrust_jet.accelerating = False

	# check for da booms
	def collisions(self):

		# ship laser hit rock?
		new_rocks = []
		ship_hit, saucer_hit = False, False

		# rocks
		for rock in self.rocks:
			rock_hit = False

			if not self.ship.in_hyperspace and rock.collide_with(self.ship):
				p = rock.check_collision(self.ship)
				if p is not None:
					ship_hit = True
					rock_hit = True

			if self.saucer is not None:
				if rock.collide_with(self.saucer):
					saucer_hit = True
					rock_hit = True

				if self.saucer.bullet_collision(rock):
					rock_hit = True

				if self.ship.bullet_collision(self.saucer):
					saucer_hit = True
					self.score += self.saucer.score_value

			if self.ship.bullet_collision(rock):
				rock_hit = True

			if rock_hit:
				self.rocks.remove(rock)
				self.stage.sprite_list.remove(rock)

				if rock.rock_type == rock.large_rock:
					play_sound('explode1')
					new_rock_type = rock.medium_rock
					self.score += 50
				elif rock.rock_type == rock.medium_rock:
					play_sound('explode2')
					new_rock_type = rock.small_rock
					self.score += 100
				else:
					play_sound('explode3')
					self.score += 200

				if rock.rock_type != rock.small_rock:
					# new rocks
					for _ in range(0,2):
						position = Vector2d(rock.position.x, rock.position.y)
						new_rock = Rock(self.stage, position, new_rock_type)
						self.stage.add_sprite(new_rock)
						self.rocks.append(new_rock)

				self.create_debris(rock)

		# saucer lasers
		if self.saucer is not None:
			if not self.ship.in_hyperspace:
				if self.saucer.bullet_collision(self.ship):
					ship_hit = True

				if self.saucer.collide_with(self.ship):
					ship_hit = True
					saucer_hit = True

			if saucer_hit:
				self.create_debris(self.saucer)
				self.kill_saucer()

		if ship_hit:
			self.kill_ship()

	def kill_ship(self):
		stop_sound('thrust')
		play_sound('explode2')
		self.exploding_count = 0
		self.lives -= 1
		if (self.lives_list):
			ship = self.lives_list.pop()
			self.stage.remove_sprite(ship)

		self.stage.remove_sprite(self.ship)
		self.stage.remove_sprite(self.ship.thrust_jet)
		self.game_state = 'exploding'
		self.ship.explode()

	def kill_saucer(self):
		stop_sound('lsaucer')
		stop_sound('ssaucer')
		play_sound('explode2')
		self.stage.remove_sprite(self.saucer)
		self.saucer = None

	def create_debris(self, sprite):
		for _ in xrange(0, 25):
			position = Vector2d(sprite.position.x, sprite.position.y)
			debris = Debris(position, self.stage)
			self.stage.add_sprite(debris)

	def display_FPS(self):
		font2 = pygame.font.Font(None, 15)
		FPS_str = str(self.fps)
		score = font2.render(FPS_str, True, (255, 255, 255))
		score_rect = score_text.get_rect(centerx=(self.stage.width/2), centery=15)
		self.stage.screen.blit(score, score_rect)

	def check_score(self):
		if self.score > 0 and self.score > self.next_life:
			play_sound('extralife')
			self.next_life += 10000
			self.add_life(self.lives)

# script to run game
if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print ' Warning, sound disabled'

init_sound_manager()
game = Asteroids()
game.play_game()