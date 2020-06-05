import pygame as pg
import math
import time
PURPLE = (255, 0, 255, 255)
#class for a player
class Character:

    def __init__(self, x, y, scale, path="assets/sprites/protoPlayer/"):

        #coordinates
        self.x = x
        self.y = y
        #initialize dimensions
        self.w = 0
        self.h = 0
        #center coordinates for collision detection
        self.cx = self.x + self.w//2
        self.cy = self.y + self.h//2
        #change in x
        self.velocity = 0
        self.maxVelocity = 3
        #change in y
        self.fallVelocity = 0
        self.maxFallVelocity = 10
        #jump velocity and jump acceleration
        self.jumpVelocity = 0
        self.jumpAccel = 0.5
        self.maxJumpVelocity = -3.5
        #causes drifting when player stops moving left or right
        self.acceleration = 0.2
        self.deceleration = 0.1

        self.scale = scale
        self.index = 0
        self.path = path
        #dict of sprites
        self.sprites = {}

        #fill dictionary with sprite lists
        self.loadSpriteList("idleRight", "moveRight/", 0, 1, 1)
        self.loadSpriteList("idleLeft", "moveLeft/", 0, 1, 1)
        self.loadSpriteList("moveRight", "moveRight/", 1, 9, 3)
        self.loadSpriteList("moveLeft", "moveLeft/", 1, 9, 3)
        self.loadSpriteList("meleeRight", "meleeRight/", 1, 6, 2)
        self.loadSpriteList("meleeLeft", "meleeLeft/", 1, 6, 2)
        self.loadSpriteList("jumpRight", "jumpRight/", 0, 2, 1)
        self.loadSpriteList("jumpLeft", "jumpLeft/", 0, 2, 1)


        #current sprite key that will be used in draw
        self.currentKey = "idleRight"

        #movement and attack booleans

        #booleans to determine if moving left or right
        self.right = False
        self.left = False
        #down determines if the s key has been pressed
        self.down = False
        #booleans that tell if player stopped moving left or right
        self.stoppedRight = False
        self.stoppedLeft = False
        #booleans to determine if attacking left or right
        self.meleeRight = False
        self.meleeLeft = False
        #boolean to make player jump
        self.jump = False
        #player must be on ground to jump
        self.onGround = False


    #key is the keyname for self.sprites entry, extension is the extra path to the base file path, l is the lower bound,
    #u is the upper bound
    #of iterations, and repeats is the number of appends per iteration
    def loadSpriteList(self, key, extension, l, u, repeats):

        lst = []
        for i in range(l, u):

            #list append process

            #load image at file path
            image = pg.image.load(self.path+extension+str(i)+".png")
            #get the size
            w, h = image.get_size()
            #specify scale of the image
            width = int(round(w*self.scale, 0))
            height = int(round(h*self.scale, 0))
            #transform the scale
            image = pg.transform.scale(image, (width, height))
            #append it to the list
            for r in range(repeats):
                lst.append(image)

            d = {key: lst}
            self.sprites.update(d)


class Player(Character):

    def __init__(self, *args, **kwargs):

        super(Player, self).__init__(*args, **kwargs)

    def handleKeyPressed(self, event):

        #if D is pressed
        if event.key == pg.K_d:
            #set every action to false except move right
            self.right = True
            self.left = False
            self.meleeRight = False
            self.meleeLeft = False
            self.currentKey = "moveRight"

        if event.key == pg.K_a:
            #set every action to false except move left
            self.right = False
            self.left = True
            self.meleeRight = False
            self.meleeLeft = False
            self.currentKey = "moveLeft"

        if event.key == pg.K_s:

            self.down = True

        if event.key == pg.K_SPACE:

            if self.onGround:

                self.jump = True


    def handleKeyReleased(self, event):

        if event.key == pg.K_d:
                #we stopped moving in the right direction
                self.right = False
                self.stoppedRight = True
                # self.index = 0
                # self.currentKey = "idleRight"

        if event.key == pg.K_a:
            #we stopped moving in the left direction
            self.left = False
            self.stoppedLeft = True
            # self.index = 0
            # self.currentKey = "idleLeft"

    #handle user input
    def handleEvents(self, event):

        if event.type == pg.KEYDOWN:

            self.handleKeyPressed(event)
        if event.type == pg.KEYUP:

            self.handleKeyReleased(event)



    #draw the player
    def draw(self, screen):

        if ((self.right or self.left or self.meleeRight or self.meleeLeft) and self.onGround):

            self.index += 1
        #if we are moving right or left
        if (self.right or self.left):

            self.index %= 24
        #if we are melee attacking
        if (self.meleeRight or self.meleeLeft):

            self.index %= 10

        #get the current sprite and it's destination rect to blit to screen
        #try and except block in case the player switches keys too fast
        try:
            #get the appropriate sprite
            sprite = self.sprites[self.currentKey][self.index]
            #get the rectangle of sprite
            spriteRect = self.sprites[self.currentKey][self.index].get_rect()
            #set spriteRect x and y to class x and y
            spriteRect.x = self.x
            spriteRect.y = self.y
            #set class width and height to spriteRect width and height
            self.w = spriteRect.width
            self.h = spriteRect.height
            screen.blit(sprite, spriteRect)
        except:

            self.index = 0
            sprite = self.sprites[self.currentKey][self.index]
            spriteRect = self.sprites[self.currentKey][self.index].get_rect()
            spriteRect.x = self.x
            spriteRect.y = self.y
            #set class width and height to spriteRect width and height
            self.w = spriteRect.width
            self.h = spriteRect.height
            screen.blit(sprite, spriteRect)

        #player velocity is always added to x
        self.x += self.velocity
        #player fall velocity is alwayes added to y
        self.fallVelocity += self.jumpVelocity
        self.y += self.fallVelocity

        #update center of sprite every draw cycle
        self.cx = self.x + self.w//2
        self.cy = self.y + self.h//2
        # pg.draw.rect(screen, PURPLE, (self.x, self.y, 5, 5))
        # pg.draw.rect(screen, PURPLE, (self.x+self.w-5, self.y, 5, 5))
        # pg.draw.rect(screen, PURPLE, (self.cx-5, self.cy, 5, 5))
        # pg.draw.rect(screen, PURPLE, (self.x + self.w - 5, self.y + self.h - 5, 5, 5))
        # pg.draw.rect(screen, PURPLE, (self.x, self.y+self.h-5, 5, 5))

        

