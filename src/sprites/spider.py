import pygame, pymunk

class Spider(pygame.sprite.Sprite):
    """A spider sprite with cool top down movement
    """

    def __init__(self, game):
        super().__init__((game.sprites, game.screen.spritelayer))

        self.body = pymunk.Body(350, 2)
        torso = [
            (10, 0),
            (30, 0),
            (0, 50),
            (40, 50)
        ]
        self.torso = pymunk.Poly(self.body, torso)

        feet = []
        for x in range(4):
            body = pymunk.Body(20, 2)
            feet.append(pymunk.Circle(body, 4))
        
    def update(self):
        pass

    def draw(self, transform=None):
        pass