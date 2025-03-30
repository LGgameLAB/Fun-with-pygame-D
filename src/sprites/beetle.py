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

        self.leg_mounts = [0 for i in range(6)]
        self.feet = [0 for i in range(6)]
        self.feet_dist_x = 13
        self.feet_dist_y = 13
        self.legs = [Leg((0,0), (15,0)) for i in range(6)]
        for l in self.legs:
            l.color = (40, 40, 40)
        self.offset = Vec(-15, 0)
        self.phase_offset = 5
        self.travel = 2.5
        
        self.angle = -135
        self.chain = SimpleChain(game, 3, [15, 18])
        self.chain.pos = self.pos
        
        names = ["head", "body", "butt"]
        self.images = [
           pygame.image.load("data/beetle_" + name + ".png") for name in names 
        ]
        
    def update(self):
        self.pos += self.dir
        self.dir.rotate_ip(0.5)
        self.angle = self.dir.as_polar()[1]
        self.chain.pos = self.pos
        self.chain.update()

        i=0
        for c in self.chain.chain:
            angle = self.angle if i == 0 else self.chain.chain_angles[int(i/2)] + 180
            # Distance from center of segment
            dist = Vec(1, 0).rotate(angle)*10
            
            # place the leg on the side of segment and place foot
            leg_mount = c + dist.rotate(-90)
            foot = c + dist.rotate(-90) * self.travel + dist*self.travel*0.5 #Place further out
            self.legs[i].update(leg_mount, foot, self.phase_offset if i%3 else 0)
            self.leg_mounts[i] = leg_mount
            self.feet[i] = foot
            
            i += 1
            # Repeat for other side of segment
            leg_mount = c + dist.rotate(90)
            foot = c + dist.rotate(90) * self.travel + dist*self.travel*0.5
            self.legs[i].update(leg_mount, foot, self.phase_offset)
            self.leg_mounts[i] = leg_mount
            self.feet[i] = foot
            i += 1


    def draw(self, surf, transform=None):
        for l in self.legs:
            l.draw(surf, transform)

        for i in range(len(self.images)):
            angle = -self.chain.chain_angles[i] + 90 if i > 0 else -self.angle - 90
            image = pygame.transform.rotate(self.images[i], angle)
            rect = image.get_rect(center = image.get_rect(center = self.chain.chain[i]).center)
 
            surf.blit(image, rect)
            
        

        # for f in self.feet:
        #      pygame.draw.circle(surf, WHITE, f, 2)
        #
        # for f in self.leg_mounts:
        #      pygame.draw.circle(surf, WHITE, f, 2)

# class Leg:
#     """A spider leg driven by inverse kinematics
#     """
#
#     def __init__(self, length, start):
#         start = Vec(start)
#         segment = Vec(length, 0)
#
#         self.points = [start, start + segment.rotate(-45), start + (math.sqrt(2)*lengt, 0)]
#         self.speed = 2
#         self.range = 22
#         self.start = Vec(0, 0)
#         self.target = Vec(0, 0)
#         self.focus = Vec(150, -200)
#         self.return_mode = True
#         self.phase = 0
#         self.reset = True
#         self.color = WHITE
#
#
#     def update(self, start, target, phase = 0):
#         self.phase += 1
#
#         if self.reset:
#             fabrik(self.points, self.focus)
#             self.target = target
#             self.phase = 0
#             self.reset = False
#             self.return_mode = False
#
#         if self.phase < phase:
#             self.target = target
#
#         for p in self.points:
#             p += start-self.start
#         self.start = start
#
#         fabrik(self.points, self.target)
#
#         if self.return_mode:
#             self.target += (target-self.target).normalize()*self.speed 
#             if self.target.distance_to(target) < 1:
#                 self.return_mode = False
#         elif self.target.distance_to(target) > self.range:
#             self.return_mode = True 
#
#     def draw(self, surf, transform=None):
#         for i in range(1, len(self.points)):
#             prev = self.points[i-1]
#             cur = self.points[i]
#             pygame.draw.aaline(surf, self.color, prev, cur, 3)
