import pygame as pg

#base class for game tiles
class Tile:

    def __init__(self, x, y, scale, path=None):

        self.x = x
        self.y = y
        #image file path
        self.path = path
        self.image = pg.image.load(path)
        w, h = self.image.get_size()
        width = int(round(w*scale, 0))
        height = int(round(h*scale, 0))
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        #get width and height of tile
        self.w = self.rect.width
        self.h = self.rect.height
    #checks if the tile is on screen to save framerate
    def onScreen(self, w, h):

        if self.x > -self.rect.width and self.x < w + self.rect.width \
            and self.y > -self.rect.height and self.y < h + self.rect.height:

            return True
        return False

    #checks if the tile is in the player's range
    def inPlayerRange(self, player):

        #if the tile is within 4 player widths of the player and 4 player heights then return True
        if self.x > player.cx - player.w*4 and self.x < player.cx + player.w*4 and \
            self.y > player.cy - player.h*4 and self.y < player.cy + player.h*4:

            return True

    #draw the tile on screen
    def draw(self, screen):

        #uodate the destination location every frame
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)