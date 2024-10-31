import pygame, pymunk
import pytweening
from pygame import Vector2 as Vec
from src.settings import *

class Spider(pygame.sprite.Sprite):
    """A spider sprite with cool top down movement
    """

    def __init__(self, game):
        super().__init__((game.sprites, game.screen.spritelayer))

        self.body = pymunk.Body(350000, 20000)
        torso = [
            (10, 20),
            (-10, 20),
            (20, -30),
            (-20, -30)
        ]
        self.torso = pymunk.Poly(self.body, torso)

        self.leg_mounts = [0 for i in range(4)]
        self.feet = [0 for i in range(4)]
        
        self.body.position = (400, 200)
        game.world.add((self.body, self.torso))
        
    def update(self):
        i=0
        for x in range(-20, 21, 40):
            for y in range(-30, 31, 60):
                pos = Vec(x, y).rotate_rad(self.body.angle)
                self.leg_mounts
                self.feet[i] = pos + self.body.position
                i+=1

    def draw(self, surf, transform=None):
        for f in self.feet:
            pygame.draw.circle(surf, WHITE, f, 3)

class leg:
    """A spider leg driven by inverse kinematics
    """

    def __init__(self, start, end):
        self.points = [Vec(p) for p in [start, pytweening.getLinePoint(*start, *end, 0.75), pytweening.getLinePoint(*start, *end, 1.5)] ]
        self.angles = [0, 0]
        self.rel_vectors = [self.points[i]-self.points[i-1] for i in range(1, len(self.points))]
        
        self.speed = 50
        self.target = Vec(0, 0)
        self.return_mode = False

    def inverse_kinematics(self):
        target = self.target

        speed = self.speed

        p2 =self.points[2]
        p1 = self.points[1]
        p0 = self.points[0]

        angle_1 = (p2-p1).angle_to(target-p1)
        p1_predicted = p1 + (p2-p1).rotate(angle_1)
        angle_1 = pygame.math.clamp(angle_1, -1*speed, speed)
        self.angles[1] += angle_1

        angle_2 = (p1_predicted-p0).angle_to(target-p0) 
        angle_2 = pygame.math.clamp(angle_2, -1*speed, speed)
        self.angles[0] += angle_2

        cumulative_angle = self.angles[0]
        self.points[1] = p0 + self.rel_vectors[0].rotate(cumulative_angle)
        cumulative_angle += self.angles[1]
        self.points[2] = p1 + self.rel_vectors[1].rotate(cumulative_angle)

        if self.points[2].distance_to(target) < 1:
            self.return_mode = False

    def update(self, target):
        if self.points[2].distance_to(target) > self.range:
            self.return_mode = True
        
        if self.return_mode:
            self.inverse_kinematics