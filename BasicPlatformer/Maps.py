import pygame as pg

#base class for map objects that store maps
class Map:

    def __init__(self, tilesDict=None, itemsList=None, player=None, npcs=None, backdrops=None):

        #for now we will store game tiles, items, the player, non-player characters (hostile and peaceful), and backgrounds
        self.tilesDict = tilesDict
        self.itemsList = itemsList
        self.player = player
        self.npcs = npcs
        self.backdrops = backdrops

    def handleEvents(self, event):

        self.player.handleEvents(event)

    def draw(self, screen):

        #tiles are drawn in physics engine object
        for key in self.tilesDict.keys():

            self.tilesDict[key].draw(screen)

        self.player.draw(screen)
        
