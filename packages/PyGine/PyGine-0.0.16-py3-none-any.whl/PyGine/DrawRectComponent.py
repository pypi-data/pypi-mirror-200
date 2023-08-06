import PyGine.PyGinegame as Game
import pygame as pg

from PyGine.Camera import Camera
from PyGine.Component import Component
from PyGine.Transform import Transform


class DrawRectComponent(Component) :
    def __init__(self,parent,color ) :
        super().__init__(parent)
        self.parent = parent
        self.transform = parent.transform
        self.color = color

    def start(self):
        pass

    def update(self,dt) :
        pg.draw.rect(Game.get().surface, self.color,((
                                                 int(self.parent.relativeTransform.position.x - (Camera.DX+Camera.PX)*(not self.parent.fixed)),
                                                 int(self.parent.relativeTransform.position.y - (Camera.DY+Camera.PY)*(not self.parent.fixed))),
                                                 (int(self.parent.relativeTransform.scale.x * Camera.ZX if (not self.parent.fixed) else self.parent.relativeTransform.scale.x),
                                                  int(self.parent.relativeTransform.scale.y * Camera.ZY if (not self.parent.fixed) else self.parent.relativeTransform.scale.y))))

    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite
