import pygame as pg
from Tiles import Tile, StaticTile
from Maps import Map
from Entities import Character, Player
from GameEngine import PhysicsEngine
import math
import time
import sys

#colors for background
RED = (255, 0, 0, 255)
GREEN = (0, 255, 0, 255)
BLUE = (0, 0, 255, 255)
SKYBLUE = (138, 210, 255, 255)

class Application:

    def __init__(self, width=1280, height=720):

        #initialize pygame
        pg.init()
        pg.display.init()
        #width and height of screen
        self.width = width
        self.height = height
        #keeps the game running
        self.running = True
        #initialize screen
        self.screen = pg.display.set_mode(size=(self.width, self.height))
        pg.display.set_caption("Basic Platformer")
        self.sampleMap = Map(tilesDict={str(i):StaticTile(i, height-32, 0.333, path="assets/sprites/forest/forestGrass.png") for i in range(0, width, 32)}, player=Player(200, height-96, 1))
        self.sampleMap.tilesDict.update({str(i+width):StaticTile(i, height-192, 0.333, path="assets/sprites/forest/forestGrass.png") for i in range(384, 640, 32)})
        self.sampleMap.tilesDict.update({str(i+(width*2)):StaticTile(i, height-160, 0.333, path="assets/sprites/forest/forestDirt.png") for i in range(384, 640, 32)})
        self.sampleMap.tilesDict.update({str(i+(width*4)):StaticTile(576, i, 0.333, path="assets/sprites/forest/forestDirt.png") for i in range(height-96, height-32, 32)})
        #physics engine
        self.engine = PhysicsEngine(myMap=self.sampleMap)
        #game clock to cap fps
        self.clock = pg.time.Clock()
    
    
    #handles keyboard presses
    def handleEvents(self):

        #get keyboard events and mouse events
        for event in pg.event.get():

            if event.type == pg.QUIT:

                self.running = False
            self.sampleMap.handleEvents(event)
    #updates physics and camera position
    def update(self):

        self.engine.update()
    #draws sprites and graphics on screen
    def draw(self):

        #clear the screen
        self.screen.fill(SKYBLUE)
        #draw the map
        self.sampleMap.draw(self.screen)
        #flip display
        pg.display.flip()
    #main game loop
    def loop(self):

        while self.running:

            self.clock.tick(60)
            self.handleEvents()
            self.update()
            self.draw()

    def exit(self):

        pg.quit()
        quit(sys.argv)

