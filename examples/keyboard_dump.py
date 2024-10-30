import pygame
import sys

pygame.init()

win = pygame.display.set_mode((100, 100))
clock = pygame.time.Clock()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        print(event)