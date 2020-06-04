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

        for key in self.tilesDict.keys():

            if self.tilesDict[key].onScreen(screen.get_width(), screen.get_height()):

                self.tilesDict[key].draw(screen)

        self.player.draw(screen)
        
