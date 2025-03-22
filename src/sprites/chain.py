import pygame
from pygame import Vector2 as Vec
from src.settings import *

class Chain(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__((game.sprites, game.screen.spritelayer))
        self.game = game
        
        self.chain_len = 50
        self.chain_dist = 10
        self.chain = [Vec(0, i*self.chain_dist) for i in range(self.chain_len)]
        
        self.pos = Vec(20, 20) # Head position

    def update(self):
        self.pos = Vec(pygame.mouse.get_pos())
        self.update_chain()


    def update_chain(self):
        self.chain[0] = self.pos
        
        for i in range(1, len(self.chain)):
            delta = self.chain[i] - self.chain[i-1]
            self.chain[i] =  delta.normalize()*self.chain_dist + self.chain[i-1]


    def draw(self, surf, transform=None):
        for c in self.chain:
            pygame.draw.circle(surf, WHITE, c, self.chain_dist/2)


