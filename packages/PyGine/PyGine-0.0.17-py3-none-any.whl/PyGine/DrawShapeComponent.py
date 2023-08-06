import PyGine.PyGinegame as Game
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component

class DrawShapeComponent(Component) :
    def __init__(self,parent,color , shape="rect"):
        super().__init__(parent)
        self.shape = shape
        self.parent = parent
        self.transform = parent.transform
        self.color = color

    def start(self):
        pass

    def update(self,dt):
        pass
    def getSprite(self):
        return self.sprite
    def setSprite(self, sprite):
        self.sprite = sprite

