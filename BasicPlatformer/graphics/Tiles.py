import pygame as pg

#base class for game tiles
class Tile:

    def __init__(self, x, y, scale, path=None):

        self.x = x
        self.y = y
        self.scale = scale
        self.path = path
        self.image = pg.image.load(path)
        #resize sprite image
        width = int(round(self.image.width*scale, 0))
        height = int(round(self.image.height, 0))
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):

        screen.blit(self.image, self.rect)