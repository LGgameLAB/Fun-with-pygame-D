import pygame, pymunk
import src.settings as settings
import src.fx as fx
from src.sprites import Spider

class Player(pygame.sprite.Sprite):

	# movement speed and dampening rate
	speed = 220
	damp = 0.97

	def __init__(self, game):
		self.game = game
		super().__init__((game.sprites, game.screen.spritelayer))

		self.init_physics()

		# self.particles = fx.GlowParticles(game)
		# game.screen.spritelayer.add(self.particles)

		self.pet = Spider(game)

	def init_physics(self) -> None:
		"""Loads the pymunk information for the player"""

		self.body = pymunk.Body(10, 2)
		self.body.position = (400, 400)
		self.body.friction = 99
		self.shape = pymunk.Circle(self.body, 7.5, (0, 0))

		self.game.world.add(self)

	def move(self):
		keys = pygame.key.get_pressed()

		"""
		Checks key presses and sets velocity to move player
		
		uses velocity damping to control movement
		Alternative movement:
		 self.body.apply_impulse_at_local_point((0, self.speed), (0, 0))

		"""

		self.body.velocity = self.damp*self.body.velocity

		if settings.checkKey("up"):
			self.body.velocity = (self.body.velocity.x, -self.speed)
		if settings.checkKey("down"):
			self.body.velocity = (self.body.velocity.x, self.speed)
		if settings.checkKey("left"):
			self.body.velocity = (-self.speed, self.body.velocity.y)
		if settings.checkKey("right"):
			self.body.velocity = (self.speed, self.body.velocity.y)

		if self.body.velocity.length > self.speed:
			self.body.velocity = (self.body.velocity.x*0.717, self.body.velocity.y*0.717)

	def update(self) -> None:
		self.move()
		#self.particles.update_position(self.body.position)#pygame.mouse.get_pos())

		
	def draw(self, win: pygame.Surface, transform = None):
		x, y = self.body.position
		if not transform:
			pygame.draw.rect(win, settings.GREEN, (x-7.5, y-7.5, 15, 15))
		else: 
			x, y = transform(self.body.position)
			pygame.draw.rect(win, settings.WHITE, (x-7.5, y-7.5, 15, 15))
