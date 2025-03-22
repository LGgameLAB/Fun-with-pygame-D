import pygame, pymunk
import pymunk.pygame_util
import sys, os
from .settings import *
from pymunk import Vec2d
from .physics import World
from .player import Player
import src.sprites as sprites

class Screen:
    """Wrapper for pygame window
    """
#sdf
    def __init__(self, game):
        self.game = game
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.base = pygame.Surface((WIDTH, HEIGHT)).convert()
        self.spritelayer = pygame.sprite.Group()

    def refresh(self):
        self.base.fill(BLACK)

    def render(self):
        for sprite in self.spritelayer:
            sprite.draw(self.base)
        self.window.blit(self.base, (0,0))
        pygame.display.set_caption(str(round(self.game.clock.get_fps())))

class Game:
    """Game controller
    """
    def __init__(self, flags: list = []):
        self.clock = pygame.time.Clock()
        self.sprites = pygame.sprite.Group()
        self.entities = []
        self.screen = Screen(self)
        self.world = World(self)
        self.player = Player(self)
        chain = sprites.Chain(self)

    def main(self):
        self.active = True
        while self.active:
            self.get_events()
            self.update()
            self.render()
            self.clock.tick(FPS)

    def update(self):
        self.world.update()
        self.sprites.update()

    def render(self):
        self.screen.refresh()
        self.world.render()
        self.screen.render()
        pygame.display.update()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.active = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                self.display.new_context()
