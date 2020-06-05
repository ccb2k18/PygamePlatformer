import pygame as pg

RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
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

    #checks if the tile is in the character's range
    def inCharacterRange(self, character):

        #if the tile is within 4 character widths of the character and 4 character heights then return True
        if self.x > character.cx - character.w*4 and self.x < character.cx + character.w*4 and \
            self.y > character.cy - character.h*4 and self.y < character.cy + character.h*4:

            return True

    #draw the tile on screen
    def draw(self, screen):

        #uodate the destination location every frame
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)
        # pg.draw.rect(screen, GREEN, (self.x, self.y, 5, 5))
        # pg.draw.rect(screen, GREEN, (self.x+self.w-5, self.y, 5, 5))
        # pg.draw.rect(screen, GREEN, (self.x, self.y+self.h-5, 5, 5))
        # pg.draw.rect(screen, GREEN, (self.x+self.w-5, self.y+self.h-5, 5, 5))

#tiles that don't move and aren't affected by physics
class StaticTile(Tile):

    def __init__(self, *args, **kwargs):

        super(StaticTile, self).__init__(*args, **kwargs)


class Platform(Tile):

    def __init__(self, *args, **kwargs):

        super(Platform, self).__init__(*args, **kwargs)