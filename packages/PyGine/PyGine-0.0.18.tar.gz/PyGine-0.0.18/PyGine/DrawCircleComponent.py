import PyGine.PyGinegame as Game
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component
from PyGine.Transform import Transform


class DrawCircleComponent(Component) :
    def __init__(self,parent,color,InitialRadius=1 ) :
        super().__init__(parent)
        self.parent = parent
        self.transform = Transform()
        self.transform.scale.x = InitialRadius
        self.color = color

    def start(self):
        pass

    def update(self,dt) :
        pg.draw.circle(Game.get().surface,self.color,(int((self.parent.relativeTransform.position.x + self.transform.position.x) - (Camera.DX+Camera.PX)*(not self.parent.fixed)),
                         int((self.parent.relativeTransform.position.y +self.transform.position.y) - (Camera.DY+Camera.PY)*(not self.parent.fixed)) ) , self.parent.relativeTransform.scale.x*Camera.ZX if (not self.parent.fixed) else self.parent.relativeTransform.scale.x)


    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite