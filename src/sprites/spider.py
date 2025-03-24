import pygame, pymunk
import pytweening
from pygame import Vector2 as Vec
from src.settings import *
from .fabrik import fabrik

class Spider(pygame.sprite.Sprite):
    """A spider sprite with cool top down movement
    """

    def __init__(self, game):
        super().__init__((game.sprites, game.screen.spritelayer))

        self.body = pymunk.Body(3500, 200000)
        torso = [
            (10, 20),
            (-10, 20),
            (20, -30),
            (-20, -30)
        ]
        self.torso = pymunk.Poly(self.body, torso)

        self.leg_mounts = [0 for i in range(4)]
        self.feet = [0 for i in range(4)]
        self.legs = [Leg((0,0), (35,0)) for i in range(4)]
        print("angles fixed")
        
        self.body.position = (150, 20)
        self.body.velocity = (0, 20)
        # self.body.apply_impulse_at_local_point((0, -1400), (20, 0))
        game.world.add((self.body, self.torso))
        
    def update(self):
        i=0
        for x in range(-20, 21, 40):
            for y in range(-20, 21, 40):
                pos = Vec(x, y).rotate_rad(self.body.angle)
                self.leg_mounts[i] = pos + self.body.position
                self.feet[i] = pos*2 + self.body.position
                self.legs[i].update(self.leg_mounts[i], self.feet[i])
                if pygame.mouse.get_pressed()[0]:
                    self.legs[i].reset = True
                i+=1
        
        #self.body.position = (150, self.body.position[1]+0.3)#pygame.mouse.get_pos()


    def draw(self, surf, transform=None):
        # for f in self.feet:
        #     pygame.draw.circle(surf, WHITE, f, 3)
        
        for l in self.legs:
            l.draw(surf, transform)

class Leg:
    """A spider leg driven by inverse kinematics
    """

    def __init__(self, start, end):
        self.points = [Vec(p) for p in [start, pytweening.getPointOnLine(*start, *end, 0.75), pytweening.getPointOnLine(*start, *end, 1.5)] ]
        self.speed = 2
        self.range = 25
        self.start = Vec(0, 0)
        self.target = Vec(0, 0)
        self.focus = Vec(150, -200)
        self.return_mode = True
        self.reset = True


    def update(self, start, target):
        if self.reset:
            fabrik(self.points, self.focus)
            self.target = target
            self.reset = False
            self.return_mode = False

        for p in self.points:
            p += start-self.start
        self.start = start

        fabrik(self.points, self.target)
        
        if self.return_mode:
            self.target += (target-self.target).normalize()*self.speed 
            if self.target.distance_to(target) < 1:
                self.return_mode = False
        elif self.target.distance_to(target) > self.range:
            self.return_mode = True 

    def draw(self, surf, transform=None):
        for i in range(1, len(self.points)):
            prev = self.points[i-1]
            cur = self.points[i]
            pygame.draw.aaline(surf, WHITE, prev, cur)


class Bioarm(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__([game.sprites, game.screen.spritelayer])
        
        length = 10
        self.points = [Vec(100 + 10*i, 100) for i in range(length)]
    
    def update(self):
        fabrik(self.points, Vec(pygame.mouse.get_pos()))
    
    def draw(self, surf, transform=None):
        # for f in self.points:
        #     pygame.draw.circle(surf, WHITE, f, 3)
        for i in range(1, len(self.points)):
            prev = self.points[i-1]
            cur = self.points[i]
            pygame.draw.aaline(surf, WHITE, prev, cur)



