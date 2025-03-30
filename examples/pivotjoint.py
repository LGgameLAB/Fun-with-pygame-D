import pymunk
import pymunk.pygame_util
import pygame

WIDTH, HEIGHT = 800, 600
CHAIN_LEN = 50
CHAIN_DIST = 10

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 0)

# Draw options for pymunk
draw_options = pymunk.pygame_util.DrawOptions(screen)

# Create a static anchor point
anchor = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
anchor.position = (WIDTH // 2, HEIGHT // 2)

# Create chain links
chain_links = []
for i in range(CHAIN_LEN):
    body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, CHAIN_DIST / 2))
    body.position = (anchor.position[0], anchor.position[1] + i * CHAIN_DIST)
    shape = pymunk.Circle(body, CHAIN_DIST / 2)
    shape.friction = 0.5
    space.add(body, shape)
    chain_links.append(body)

# Add constraints between chain links using SlideJoint
for i in range(1, CHAIN_LEN):
    joint = pymunk.SlideJoint(chain_links[i - 1], chain_links[i], (0, 0), (0, 0), CHAIN_DIST, CHAIN_DIST)
    space.add(joint)

# Attach first link to anchor
space.add(pymunk.SlideJoint(anchor, chain_links[0], (0, 0), (0, 0), CHAIN_DIST, CHAIN_DIST))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the first link to follow the mouse
    anchor.position = pygame.mouse.get_pos()

    space.step(1/60)  # Physics update
    screen.fill((0, 0, 0))
    space.debug_draw(draw_options)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

