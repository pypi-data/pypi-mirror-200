from abc import ABC

import pygame as pg
from PyGine import PhysicCollisionModule
import PyGine.Debug as Debug

from PyGine.Scene import Scene
from PyGine.ImageLibrary import ImageLibrary
from PyGine.DefaultScene import DefaultScene


class PyGineGame(ABC) :

    game = None
    def __init__(self, width, height,game) :

        PyGineGame.game = game
        pg.init()
        pg.event.set_allowed([pg.QUIT])
        self.width = width
        self.height = height
        self.surface = pg.Surface((width, height))
        self.FEN = pg.display.set_mode((width, height),  pg.DOUBLEBUF)
        self.running = True
        self.clock = pg.time.Clock()
        self.fps = 600
        self.dt = 0
        self.CurrentScene = None
        self.CurrentSceneID = 0
        self.scenes = []
        self.ShowHitbox = False
        self.BG_COLOR = (0,0,0)

        PhysicCollisionModule.PhysicCollisionModule()

        pg.display.set_caption("PyGine Window")
        #mandatory
        self.imageLib = None
        
        self.addScene(DefaultScene())
        self.setScene(0)

    def setBgColor(self,color):
        self.BG_COLOR = color

    def run(self):
        while self.running:
            self.dt = self.clock.tick(self.fps)
            self.Mupdate()
            self.FEN.blit(self.surface, (0, 0))
            pg.display.flip()

    def setImageLibFolder(self,path):
        self.imageLib = ImageLibrary(path)


    def update(self):
        pass

    def setCaption(self,caption):
        pg.display.set_caption(caption)


    def Mupdate(self):
        

        self.surface.fill(self.BG_COLOR)

        PhysicCollisionModule.instance().Update()
        self.update()
        for e in pg.event.get() :
            if e.type == pg.QUIT :
                exit()
        self.CurrentScene.Mupdate(self.dt)
        Debug.resetCalculation()


    def setScene(self, ID):
        if self.CurrentScene :
            self.CurrentScene.Mend()
        self.CurrentSceneID = ID
        self.CurrentScene = self.scenes[ID]
        self.CurrentScene.Mstart()


    def instanciate(self,obj):
        self.getCurrentScene().addGameObject(obj)
        return obj

    def getSceneID(self):
        return self.CurrentSceneID

    def getCurrentScene(self)->Scene:
        return self.CurrentScene

    def addScene(self,scene):
        self.scenes.append(scene)


def get():
    return PyGineGame.game
