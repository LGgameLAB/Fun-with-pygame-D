import pygame
import sys
import random

pygame.init()

win = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

particles = []

def add_particle(x, y, size = 4, vx=0, vy=0):
    global particles
    particles.append([x, y, size, vx, vy])

def update_particle(p):
    p[2] *= 0.97
    p[1] += p[4] # Add Velocity
    p[0] += p[3]
    p[4] += 0.3 # Add acceleration
    if p[1] >= win.get_height():
        particles.remove(p)#particles.index(p))

def particle_surface(radius, color):
    surf = pygame.Surface((int(radius*2), int(radius*2)))
    pygame.draw.circle(surf, color, (radius, radius),radius)
    surf.set_colorkey((0,0,0))

    return surf

print("Wave your mouse over the window")

while True:
    clock.tick(60)
    win.fill((0,0,0))

    for x in range(10):
        add_particle(*pygame.mouse.get_pos(), 10, (random.random()-0.5)*3, -(random.random())*5)
    for p in particles:
        update_particle(p)
        pygame.draw.circle(win, (255,255,255), (p[0], p[1]), p[2])
        
        # Glow Effect
        r = p[2]*2
        win.blit( particle_surface( r, (30,30,30) ), (p[0]-r, p[1]-r), special_flags = pygame.BLEND_RGB_ADD)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    pygame.display.set_caption("FPS: " + str(clock.get_fps()) + " | particles: " + str(len(particles)))
    pygame.display.flip()

