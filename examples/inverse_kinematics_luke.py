import sys, pygame
import time
from pygame.math import Vector2 as Vec
pygame.init()

size = width, height = 400, 400
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

points = [Vec(200, 200), Vec(250, 200), Vec(300, 200)]
target = Vec(400, 200)

rel_vectors = []
angles = []

max_angle = 360 # Adjust for limited angles

for i in range(1, len(points)):
    rel_vectors.append(points[i] - points[i-1])
    angles.append(0)

def render():
    global BLACK, WHITE

    screen.fill(BLACK)
    for i in range(1, len(points)):
        pygame.draw.aaline(screen, WHITE, points[i-1], points[i])

    for p in points:
        pygame.draw.circle(screen, WHITE, (int(p[0]), int(p[1])), 5)

    pygame.draw.circle(screen, WHITE, (int(target[0]), int(target[1])), 10)
    pygame.display.flip()

def inverse_kinematics():
    global target

    speed = 50

    p2 = points[2]
    p1 = points[1]
    p0 = points[0]

    angle_1 = (p2-p1).angle_to(target-p1)
    p1_predicted = p1 + (p2-p1).rotate(angle_1)
    angle_1 = pygame.math.clamp(angle_1, -1*speed, speed)
    angles[1] += angle_1

    angle_2 = (p1_predicted-p0).angle_to(target-p0)
    angle_2 = pygame.math.clamp(angle_2, -1*speed, speed)
    angles[0] += angle_2

    cumulative_angle = angles[0]
    points[1] = p0 + rel_vectors[0].rotate(cumulative_angle)
    cumulative_angle += angles[1]
    points[2] = p1 + rel_vectors[1].rotate(cumulative_angle)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    target = Vec(target-(200, 200)).rotate(2) + (200, 200)
    inverse_kinematics()    

    render()

    clock.tick(30)
