import pygame

WIDTH, HEIGHT = 800, 600
COLLTYPE_BALL = 2
FPS = 60
FIXED_DT = 1/FPS

def flipy(y_value):
	return HEIGHT - y_value

keySet = {
	"up": pygame.K_UP,
	"down": pygame.K_DOWN,
	"left": pygame.K_LEFT,
	"right": pygame.K_RIGHT
}
def checkKey(move):
    '''Handy Dandy class for checking the status of keys given a 
    a) keyword for the built in mapped buttons
    b) a list of pygame keys in which it returns true for any
    c) or just a single pygame key

    pygame key being pygame.K_a or pygame.K_UP'''
    keys = pygame.key.get_pressed()
    if isinstance(move, str):
        try:
            for k in keySet[move]:
                if keys[k]:
                    return True
        except TypeError:
            if keys[keySet[move]]:
                return True
    else:
        try:
            for k in move:
                if keys[k]:
                    return True
        except TypeError:
            if keys[move]:
                return True
    return False

WHITE = (255,255,255)
BLACK = (0,0,0)