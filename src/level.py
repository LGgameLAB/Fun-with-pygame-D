import pygame

class Level(pygame.sprite.Sprite):
    def __init__(self, game, file):
        self.game = game
        super().__init__(game.sprites)
        with open(file, "r") as f:
            data = f.read().split('\n')
            self.data = data
        self.tileW = 25
        self.color = (150, 0, 0)
        self.colliders = pygame.sprite.Group()
        self.startCoords = Vec(0,0)

    def load(self):
        self.render()
        self.rect = pygame.Rect(0, 0, self.image.get_width(), self.image.get_height())
    
    def update(self):        
        pass

    def render(self):
        w = len(self.data[0])*self.tileW
        h = len(self.data)*self.tileW
        self.image = pygame.Surface((w, h), pygame.SRCALPHA)
        if self.game.gravity:
            img = pygame.transform.rotate(self.arrowPic, self.game.gravity.angle_to((0, 0)))
            self.image.blit(img, img.get_rect(center=(w/2, h/2)) )
        for col in range(len(self.data)):
            for row in range(len(self.data[col])):
                value = self.data[col][row]
                if not value == "0":
                    rect = pygame.Rect(row*self.tileW, col*self.tileW, self.tileW, self.tileW)
                    if value == "s":
                        self.startCoords = Vec(rect.topleft)
                    else:
                        if Block.getblock(str(value)):
                            newblock(self.game, rect)
                        else:
                            Collider(self.game, rect)
                            pygame.draw.rect(self.image, self.color, rect, 3)
        return self.image