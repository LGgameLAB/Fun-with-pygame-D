import pygame, pymunk
import pymunk.pygame_util
import sys, os
from .settings import *
from pymunk import Vec2d
from .physics import World
from .player import Player

class Screen:
	"""Wrapper for pygame window
	"""

	def __init__(self):
		self.window = pygame.display.set_mode((WIDTH, HEIGHT))
		self.layer0 = pygame.Surface((WIDTH, HEIGHT))

	def refresh(self):
		self.layer0.fill(BLACK)

	def render(self):
		self.window.blit(self.layer0, (0,0))

class Game:
	def __init__(self, flags: list = []):
		self.clock = pygame.time.Clock()
		self.sprites = pygame.sprite.Group()
		self.entities = []
		self.screen = Screen()
		self.world = World(self)
		self.player = Player(self)

	def main(self):
		self.active = True
		while self.active:
			self.get_events()
			self.update()
			self.render()
			self.clock.tick(60)



	def update(self):
		self.world.update()
		self.sprites.update()

	def render(self):
		self.screen.refresh()
		self.world.render()
		for sprite in self.sprites:
			sprite.draw(self.screen.layer0)

		self.screen.render()
		pygame.display.update()

	def get_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.active = False
				pygame.quit()
				sys.exit()
