import pygame, pymunk
from pygame import Vector2 as Vec
from src.settings import *

class Chain(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__((game.screen.spritelayer))
        self.game = game
        self.reset = True
        
        self.chain_len = 50
        self.chain_dist = 10
        self.chain = [Vec(0, i*self.chain_dist) for i in range(self.chain_len)]
        # self.chain_links = []
        # for i in range(self.chain_len):
        #     body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, self.chain_dist / 2))
        #     body.position = tuple(self.chain[i])
        #     shape = pymunk.Circle(body, self.chain_dist / 2)
        #     shape.friction = 0.5
        #     shape.filter = pymunk.ShapeFilter(group=1)
        #     self.game.world.add((body, shape))
        #     self.chain_links.append(body)

        # for i in range(1, self.chain_len): 
        #     if i > 0:
        #         joint = pymunk.PinJoint(self.chain_links[i], 
        #                                 self.chain_links[i-1],
        #                                 (0, 0),
        #                                 (0, 0))
        #         self.game.world.space.add(joint)


        self.pos = Vec(20, 20) # Head position

    def update(self):
        self.update_chain()


    def update_chain(self):
        self.chain[0] = self.pos
       
        for i in range(1, len(self.chain)):
            delta = self.chain[i] - self.chain[i-1]
            self.chain[i] =  delta.normalize()*self.chain_dist + self.chain[i-1]

        # for i in range(self.chain_len):
        #     self.chain_links[i].position = tuple(self.chain[i])

    def draw(self, surf, transform=None):
        for c in self.chain:
            pygame.draw.circle(surf, WHITE, c, self.chain_dist/2)

class SimpleChain(pygame.sprite.Sprite):
    def __init__(self, game, length, dists):
        super().__init__((game.sprites, game.screen.spritelayer))
        self.game = game
        self.reset = True
        
        self.chain_len = length
        self.chain_distances = dists
        self.chain = [Vec(0, i*self.chain_distances[i-1]) for i in range(self.chain_len)]
        self.chain_angles = [0.0 for i in range(self.chain_len)]
        
        self.pos = Vec(20, 20) # Head position

    def update(self):
        self.update_chain()


    def update_chain(self):
        self.chain[0] = self.pos
       
        for i in range(1, len(self.chain)):
            delta = self.chain[i] - self.chain[i-1]
            self.chain[i] =  delta.normalize()*self.chain_distances[i-1] + self.chain[i-1]
            self.chain_angles[i] = delta.as_polar()[1]

    def draw(self, surf, transform=None):
        # for i in range(len(self.chain)):
        #     pygame.draw.circle(surf, WHITE, self.chain[i], 5)#self.chain_distances[i]/2)
        pass
        
