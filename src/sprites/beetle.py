import pygame, pymunk
from pygame import Vector2 as Vec
from src.settings import *
from .fabrik import fabrik
from .spider import Leg
from .chain import SimpleChain

class Beetle(pygame.sprite.Sprite):
    """A spider sprite with cool top down movement
    """

    def __init__(self, game):
        super().__init__((game.sprites, game.screen.spritelayer))
        
        self.pos = Vec((300, 300))
        self.dir = Vec(1,0)

        self.leg_mounts = [0 for i in range(4)]
        self.feet = [0 for i in range(4)]
        self.feet_dist_x = 13
        self.feet_dist_y = 13
        self.legs = [Leg((0,0), (15,0)) for i in range(4)]
        self.offset = Vec(-15, 0)
        self.travel = 1.8
        
        self.angle = -135
        self.chain = SimpleChain(game, 3, [15, 18])
        self.chain.pos = self.pos
        
        names = ["head", "body", "butt"]
        self.images = [
           pygame.image.load("data/beetle_" + name + ".png") for name in names 
        ]
        
    def update(self):
        i=0
        for x in range(-self.feet_dist_x, self.feet_dist_x+1, self.feet_dist_x*2):
            for y in range(-self.feet_dist_y, self.feet_dist_y+1, self.feet_dist_y*2):
                pos = Vec(x, y).rotate(self.angle) + self.offset.rotate(self.angle)
                self.leg_mounts[i] = pos + self.pos
                self.feet[i] = pos*self.travel + self.pos
                self.legs[i].update(self.leg_mounts[i], self.feet[i])
                if pygame.mouse.get_pressed()[0]:
                    self.legs[i].reset = True
                i+=1

        self.dir = (Vec(pygame.mouse.get_pos()) - self.pos)
        if self.dir.length() > 0.1:
            self.angle = self.dir.as_polar()[1]
        self.pos = pygame.mouse.get_pos()
        self.chain.pos = self.pos


    def draw(self, surf, transform=None):
        for i in range(len(self.images)):
            angle = -self.chain.chain_angles[i] + 90 if i > 0 else -self.angle - 90
            image = pygame.transform.rotate(self.images[i], angle)
            rect = image.get_rect(center = image.get_rect(center = self.chain.chain[i]).center)
 
            surf.blit(image, rect)
            
        # for l in self.legs:
        #     l.draw(surf, transform)
        #
        # for f in self.feet:
        #      pygame.draw.circle(surf, WHITE, f, 3)


