import pygame as pg
import math
import time

class GameCamera:

    def __init__(self):

        pass

class PhysicsEngine:

    def __init__(self, myMap=None, gravity=0.4):
        #map for physics engine to modify/update
        self.myMap = myMap
        #gravity that acts upon all characters and dynamic tiles
        self.gravity = gravity
    #apply the proper velocity to move the player
    def applyPlayerVelocity(self):

        player = self.myMap.player

        #if the player is moving right
        if player.right:

            if player.velocity < player.maxVelocity:

                player.velocity += player.acceleration
        #if the player is moving left
        if player.left:

            if player.velocity > -player.maxVelocity:

                player.velocity -= player.acceleration

    #applies some resistances when the player stops moving
    def removePlayerVelocity(self):

        player = self.myMap.player

        #if the player stopped moving right
        if player.stoppedRight:

            #if the player stopped right then stopped left should be false
            player.stoppedLeft = False
            #if the player is still moving right
            if player.velocity > 0:
                #slowly slow down the player
                player.velocity -= player.deceleration
            #when the player has stopped, set stopped right to false
            if player.velocity < 0:

                player.velocity = 0
                player.stoppedRight = False
        #if the player stopped moving left
        #follows same formula as stopped right
        if player.stoppedLeft:
            #if the player stopped left then stopped right should be false
            player.stoppedRight = False
            if player.velocity < 0:

                player.velocity += player.deceleration
            if player.velocity > 0:

                player.velocity = 0
                player.stoppedLeft = False
    #check if the player center x coord is between a tile
    def playerCenterXInBetweenTile(self, tile):

        player = self.myMap.player
        #if the center x coord of the player is in between the tile return True 
        if player.cx > tile.x and player.cx < tile.x + tile.w:

            return True

    #detect if the player is on the ground, and if so adjust player parameters
    def detectPlayerGrounded(self):

        player = self.myMap.player
        tiles = self.myMap.tilesDict
        for key in tiles.keys():
            #if the tile is in close proximity to the player
            if tiles[key].inPlayerRange(player):
                #if the center x of player is in between tile and the bottom of the player is past the tile surface
                if self.playerCenterXInBetweenTile(tiles[key]) and (player.y + player.h) >= tiles[key].y:
                    player.fallVelocity = 0
                    player.y = tiles[key].y - player.h
                    player.onGround = True


    def applyPlayerJump(self):

        player = self.myMap.player
        if player.jump:
            #if the player is jumping then obviously they aren't on the gorund
            player.onGround = False
            if player.jumpVelocity > player.maxJumpVelocity:

                player.jumpVelocity -= player.jumpAccel
            if player.jumpVelocity <= player.maxJumpVelocity:

                player.jumpVelocity = 0
                player.jump = False

    def applyPlayerGravity(self):

        player = self.myMap.player
        #if the player isn't on the ground apply gravity
        if not player.onGround:
            #if we haven't reached our terminal fall velocity
            if player.fallVelocity < player.maxFallVelocity:
                #keep applying acceleration
                player.fallVelocity += self.gravity
            if player.fallVelocity >= player.maxFallVelocity:

                player.fallVelocity = player.maxFallVelocity

    
    def update(self):

        self.applyPlayerVelocity()
        self.removePlayerVelocity()
        self.applyPlayerJump()
        self.applyPlayerGravity()
        self.detectPlayerGrounded()

