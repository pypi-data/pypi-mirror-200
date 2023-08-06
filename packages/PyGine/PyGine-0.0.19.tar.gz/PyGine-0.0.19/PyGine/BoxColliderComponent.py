import pygame as pg
from PyGine.ColliderComponent import ColliderComponent
from PyGine.Camera import Camera
import PyGine.PyGinegame as Game
from PyGine import Debug

class BoxColliderComponent(ColliderComponent) :
    def __init__(self,parent) :
        super().__init__(parent)
        self.parent = parent
        self.transform = parent.transform


    def update(self,dt) :
        if (Debug.Debug.ShowCollidersBox):
            pg.draw.rect(Game.get().surface, (0,0,0),((
                                                 int(self.transform.position.x - (Camera.PX+Camera.DX)),
                                                 int(self.transform.position.y - (Camera.PY+Camera.DY)) ),
                                                 (int(self.transform.scale.x * Camera.ZX),
                                                  int(self.transform.scale.y * Camera.ZY))),1)

    def CallCollide(self,o):
        self.parent.onCollision(o)

