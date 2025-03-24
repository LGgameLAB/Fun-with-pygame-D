import pygame
import pymunk
import pymunk.pygame_util

def create_chain(space, start_pos, num_links=10, link_length=20, link_width=5):
    bodies = []
    joints = []
    previous_body = None
    for i in range(num_links):
        body = pymunk.Body()
        body.position = start_pos[0], start_pos[1] + i * link_length
        shape = pymunk.Segment(body, (-link_width // 2, 0), (link_width // 2, 0), 2)
        shape.mass = 1
        shape.friction = 0.5
        space.add(body, shape)
        
        if previous_body:
            joint = pymunk.PinJoint(previous_body, body, (0, link_length // 2), (0, -link_length // 2))
            space.add(joint)
            joints.append(joint)
        
        bodies.append(body)
        previous_body = body
    
    return bodies, joints

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    
    # Create a chain
    chain_bodies, _ = create_chain(space, (400, 300))
    mouse_joint = None
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Attach the first chain link to the mouse position
        if mouse_joint:
            space.remove(mouse_joint)
        mouse_joint = pymunk.DampedSpring(chain_bodies[0], space.static_body, (0, 0), mouse_pos, 0, 1000, 10)
        space.add(mouse_joint)
        
        # Step physics
        space.step(1/60)
        
        # Draw everything
        screen.fill((30, 30, 30))
        space.debug_draw(draw_options)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()

