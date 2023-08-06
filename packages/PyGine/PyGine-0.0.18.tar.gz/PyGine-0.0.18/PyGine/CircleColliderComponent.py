import math

from PyGine import Debug, PyGinegame as Game

from PyGine.Camera import Camera
from PyGine.ColliderComponent import ColliderComponent
import pygame as pg
class CircleColliderComponent(ColliderComponent) :
    def __init__(self,parent) :
        super().__init__(parent)
        self.parent = parent
        self.transform = parent.transform
    def update(self,dt) :
        if(Debug.Debug.ShowCollidersBox) :
            pg.draw.circle(Game.get().surface,(0,0,0,100),(int(self.transform.position.x - (Camera.PX+Camera.DX)),
                         int(self.transform.position.y - (Camera.PY+Camera.DY)) ) , self.transform.scale.x*Camera.ZX,1)

    def CallCollide(self,o):
        self.parent.onCollision(o)

    