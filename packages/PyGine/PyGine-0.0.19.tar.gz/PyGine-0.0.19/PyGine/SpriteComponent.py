from PyGine.Component import Component
import pygame as pg
import PyGine.PyGinegame as Game
from PyGine.Camera import Camera
from PyGine.ImageLibrary import ImageLibrary
class SpriteComponent(Component) :
    def __init__(self,parent, sprite=" ") :
        super().__init__(parent)
        self.sprite = sprite
        self.parent = parent

    def start(self):
        pass

    def update(self,dt) :
        #scale the img to the transform scale
        img = pg.transform.scale(ImageLibrary.images[self.sprite], (
        int(self.parent.relativeTransform.scale.x * Camera.ZX if (not self.parent.fixed) else self.parent.relativeTransform.scale.x), int(self.parent.relativeTransform.scale.y *Camera.ZY if (not self.parent.fixed) else self.parent.relativeTransform.scale.y)))
        Game.get().surface.blit(img,((int(self.parent.relativeTransform.position.x - (Camera.DX+Camera.PX)*(not self.parent.fixed) ),int(self.parent.relativeTransform.position.y-( Camera.DY+Camera.PY)*(not self.parent.fixed)) )))

    def getSprite(self) :
        return self.sprite

    def setSprite(self, sprite) :
        self.sprite = sprite