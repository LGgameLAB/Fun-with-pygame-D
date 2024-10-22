import pygame
import sys
import random

pygame.init()

win = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

TARGET_NUM_PARTICLES = 10000

particles = []
removal = []

def add_particle(x, y, size = 4, vx=0, vy=0):
    global particles
    particles.extend([x, y, size, vx, vy])

def update_particle(i):
    particles[i + 2] *= 0.97
    particles[i + 1] += particles[i + 4] # Add Velocity
    particles[i] += particles[i + 3]
    particles[i + 4] += 0.3 # Add acceleration
    if particles[i + 1] >= win.get_height():
        #particles.remove(p)#particles.index(p))
        removal.append(i)

def particle_surface(radius, color):
    surf = pygame.Surface((int(radius*2), int(radius*2)))
    pygame.draw.circle(surf, color, (radius, radius),radius)
    surf.set_colorkey((0,0,0))

    return surf

while True:
    clock.tick(60)
    win.fill((0,0,0))

    for x in range(TARGET_NUM_PARTICLES - (len(particles) // 5)):
        add_particle(*pygame.mouse.get_pos(), 10, (random.random()-0.5)*3, -(random.random())*5)
    for chunk in range((len(particles) // 5) - 1):
        update_particle(chunk * 5)
        pygame.draw.circle(win, (255,255,255), (particles[chunk * 5], particles[chunk * 5 + 1]), particles[chunk * 5 + 2])
        
        # Glow Effect
        r = particles[chunk * 5 + 2]*2
        win.blit(
            particle_surface(r, (30,30,30)),
            (particles[chunk * 5] - r, particles[chunk * 5 + 1] - r),
            special_flags = pygame.BLEND_RGB_ADD
        )

    r_count = 0
    while len(removal) > 0:
        rem = removal.pop(0) - 5 * r_count

        # I unrolled a loop
        particles.pop(rem)
        particles.pop(rem)
        particles.pop(rem)
        particles.pop(rem)
        particles.pop(rem)

        r_count += 1


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
    print("\rFPS: "  + str(round(clock.get_fps(), 0)) + " | particles: " + str(len(particles) // 5) + "   ", end="")
    pygame.display.flip()

