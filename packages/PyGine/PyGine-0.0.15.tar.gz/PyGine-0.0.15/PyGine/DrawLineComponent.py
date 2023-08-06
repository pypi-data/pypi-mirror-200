import PyGine.PyGinegame as Game
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component
from PyGine.Transform import Transform
from PyGine.Vector3 import Vector3

class DrawLineComponent(Component) :
    def __init__(self,parent,color,start_= Vector3(0,0,0),end_= Vector3(0,0,0) ) :
        super().__init__(parent)
        self.parent = parent
        self.transform = parent.transform
        self.color = color
        self.start_ = start_
        self.end_ = end_

    def start(self) :
        pass

    def update(self,dt) :
        pg.draw.line(Game.get().surface, self.color, (self.start_.x,self.start_.y), (self.end_.x,self.end_.y))


    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite