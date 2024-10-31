import pygame, pymunk
import pymunk.pygame_util
import sys, os
from .settings import *
from pymunk import Vec2d

class World:
	def __init__(self, game):
		self.game = game
		self.space = pymunk.Space()
		self.space.gravity = 0.0, 0.0
		self.options = pymunk.pygame_util.DrawOptions(game.screen.base)

		# Makes a bunch of balls for funsies
		# for x in range(3):
		# 	self.space.add(*self.ball((10*x, 10*x)))
		# self.space.bodies[0].apply_impulse_at_local_point((999, 999), (0, 0))

		# Testing out a segment
		body = pymunk.Body(100, 100)
		segment = pymunk.Segment(body, (0, -10), (0, 10), 2)
		self.add((body, segment))
		body.position = (100,100)


	def ball(self, p = (20, 20)):
		body = pymunk.Body(100, 100)
		body.position = p
		shape = pymunk.Circle(body, 10, (0, 0))
		shape.friction = 0.5
		shape.collision_type = COLLTYPE_BALL
		return body, shape

	def add(self, entity):
		if isinstance(entity, pygame.sprite.Sprite):
			self.space.add(entity.body, entity.shape)
		else:
			self.space.add(entity[0], entity[1])
	
	def render(self):
		self.space.debug_draw(self.options)

	def update(self):
		# print(self.game.clock.get_time())
		# print(FIXED_DT)
		self.space.step(FIXED_DT)