import pygame as pg
from Tiles import Tile, StaticTile, Platform
import math
import time

class GameCamera:

    def __init__(self, player, centerX=640, centerY=480, sensitivity=1):

        self.sW = 1280
        self.sH = 720
        self.lowerX = centerX-(player.w*(10//sensitivity))
        self.lowerY = centerY-(player.h*(10//sensitivity))
        self.upperX = centerX+(player.w*(10//sensitivity))
        self.upperY = centerY+(player.h*(10//sensitivity))
        self.changeX = 0
        self.changeY = 0

    def shiftPlayerX(self, player):

        if player.x < self.lowerX or player.x > self.upperX:

            player.x += -player.velocity
            self.changeX = -player.velocity
            return
        self.changeX = 0

    def shiftPlayerY(self, player):

        if player.y < self.lowerY or player.y > self.upperY:

            player.y += -player.fallVelocity
            self.changeY = -player.fallVelocity
            return
        self.changeY = 0

    def shiftTile(self, tile):

        tile.x += self.changeX
        tile.y += self.changeY

class PhysicsEngine:

    def __init__(self, myMap=None, gravity=0.4):
        #map for physics engine to modify/update
        self.myMap = myMap
        #gravity that acts upon all characters and dynamic tiles
        self.gravity = gravity
        #camera to shift point of view
        self.camera = GameCamera(self.myMap.player)
    #apply the proper velocity to move the character
    def applyCharacterVelocity(self, character):

        #if the character is moving right
        if character.right:

            if character.velocity < character.maxVelocity:

                character.velocity += character.acceleration
        #if the character is moving left
        if character.left:

            if character.velocity > -character.maxVelocity:

                character.velocity -= character.acceleration

    #applies some resistances when the character stops moving
    def removeCharacterVelocity(self, character):

        #if the character stopped moving right
        if character.stoppedRight:

            #if the character stopped right then stopped left should be false
            character.stoppedLeft = False
            #character.left = False
            #if the character is still moving right
            if character.velocity > 0:
                #slowly slow down the character
                character.velocity -= character.deceleration
            #when the character has stopped, set stopped right to false
            if character.velocity < 0:

                character.velocity = 0
                character.stoppedRight = False
                if not character.left:
                    #set sprite to idle
                    character.index = 0
                    character.currentKey = "idleRight"
        #if the character stopped moving left
        #follows same formula as stopped right
        if character.stoppedLeft:
            #if the character stopped left then stopped right should be false
            character.stoppedRight = False
            #character.right = False
            if character.velocity < 0:

                character.velocity += character.deceleration
            if character.velocity > 0:

                character.velocity = 0
                character.stoppedLeft = False
                if not character.right:
                    #set sprite to idle
                    character.index = 0
                    character.currentKey = "idleLeft"
    #check if the character center x coord is between a tile
    def characterCenterXInBetweenTile(self, tile, character):

        #if the center x coord of the character is in between the tile return True 
        if (character.cx > tile.x - character.w//2) and (character.cx < tile.x + tile.w + character.w//2):

            return True
    #check if the character center y coord is between a tile
    def characterBottomInBetweenTile(self, tile, character):

        #if the bottom of the player is in between a tile
        if character.y + character.h > tile.y and character.y + character.h <= tile.y + tile.h:

            return True

    def characterTopInBetweenTile(self, tile, character):

        #if the top of the player is in between a tile
        if character.y > tile.y and character.y < tile.y + tile.h:

            return True

    #detect if the character is on the ground, and if so adjust character parameters
    def detectCharacterGrounded(self, tile, character):

        if not isinstance(tile, Platform):
            #if the tile is in close proximity to the character
            if tile.inCharacterRange(character):
                #if the center x of character is in between tile and the bottom of the character is past the tile surface
                #but only half the character's height is past the tile
                if self.characterCenterXInBetweenTile(tile, character) and ((character.y + character.h) >= tile.y) and \
                    abs((character.y + character.h) - tile.y) < character.h//4:
                    character.fallVelocity = 0
                    character.y = tile.y - character.h
                    character.onGround = True
        else:

            #if the tile is in close proximity to the character
            if tile.inCharacterRange(character):
                #if the center x of character is in between tile and the bottom of the character is past the tile surface
                #but only half the character's height is past the tile
                if self.characterCenterXInBetweenTile(tile, character) and ((character.y + character.h) >= tile.y) and \
                    abs((character.y + character.h) - tile.y) < character.h//4 and character.fallVelocity > 0:
                    character.fallVelocity = 0
                    character.y = tile.y - character.h
                    character.onGround = True



    #handles if the character is jumping from below the tile and colliding
    def handleCharacterTileCollisionBelow(self, tile, character):

        #if this tile is not a platform, because we want to be able to jump from below onto platforms
        if not isinstance(tile, Platform):

            if self.characterCenterXInBetweenTile(tile, character) and (character.y < tile.y + tile.h) and \
                abs((tile.y + tile.h) - character.y) < character.h//4:

                #if the character hits the bottom of a tile they aren't jumping anymore and consequently fall
                character.jumpVelocity = 0
                character.jump = False
                character.fallVelocity = 0
                character.y = tile.y + tile.h
    #check if the character is colliding with a tile from the left
    def handleCharacterTileCollisionLeft(self, tile, character):

        if not isinstance(tile, Platform):
        
            if (self.characterTopInBetweenTile(tile, character) or self.characterBottomInBetweenTile(tile, character)) and \
                (character.x > tile.x - character.w) and abs(character.x - (tile.x-character.w)) < character.w//4:

                character.velocity = 0
                character.left = False
                character.stoppedLeft = False
                character.x = tile.x - character.w
    #check if the character is colliding with a tile from the right
    def handleCharacterTileCollisionRight(self, tile, character):

        if not isinstance(tile, Platform):
        
            if (self.characterTopInBetweenTile(tile, character) or self.characterBottomInBetweenTile(tile, character)) and \
                (character.x < tile.x + tile.w) and abs((tile.x + tile.w) - character.x) < character.w//4:

                character.velocity = 0
                character.left = False
                character.stoppedLeft = False
                character.x = tile.x + tile.w
    
    def characterFallThroughPlatform(self, tile, character):

        if isinstance(tile, Platform):

            if self.characterCenterXInBetweenTile(tile, character) and (character.y + character.h == tile.y) and \
                character.down:

                character.y = character.y + character.h//4
                character.down = False 


    def applyCharacterJump(self, character):

        if character.jump:
            #if the character is jumping then obviously they aren't on the gorund
            character.onGround = False
            if character.jumpVelocity > character.maxJumpVelocity:

                character.jumpVelocity -= character.jumpAccel
            if character.jumpVelocity <= character.maxJumpVelocity:

                character.jumpVelocity = 0
                character.jump = False

    def applyCharacterGravity(self, character):

        #if the character isn't on the ground apply gravity
        if not character.onGround:
            #if we haven't reached our terminal fall velocity
            if character.fallVelocity < character.maxFallVelocity:
                #keep applying acceleration
                character.fallVelocity += self.gravity
            if character.fallVelocity >= character.maxFallVelocity:

                character.fallVelocity = character.maxFallVelocity

    
    def update(self, screen):

        player = self.myMap.player
        #shift camera point of view
        self.camera.changeX = 0
        self.camera.changeY = 0
        self.camera.shiftPlayerX(player)
        self.camera.shiftPlayerY(player)
        #apply the physical forces of the world on the character
        self.applyCharacterVelocity(player)
        self.removeCharacterVelocity(player)
        self.applyCharacterJump(player)
        self.applyCharacterGravity(player)
        player.onGround = False
        #do various collision checks for all tiles in range of character
        tiles = self.myMap.tilesDict
        for key in tiles.keys():

            self.camera.shiftTile(tiles[key])
            self.detectCharacterGrounded(tiles[key], player)
            self.handleCharacterTileCollisionBelow(tiles[key], player)
            self.handleCharacterTileCollisionLeft(tiles[key], player)
            self.handleCharacterTileCollisionRight(tiles[key], player)
            self.characterFallThroughPlatform(tiles[key], player)
        #print(self.characterTopInBetweenTile(player))

