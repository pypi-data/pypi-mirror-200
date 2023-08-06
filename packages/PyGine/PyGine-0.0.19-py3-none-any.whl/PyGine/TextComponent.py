from PyGine.Camera import Camera
from PyGine.Component import Component
import PyGine.PyGinegame as Game
import pygame as pg
from PyGine.Transform import Transform

class TextComponent(Component) :
    def __init__(self, parent,text = " ",color = (255,0,255),size = 32):
        super().__init__(parent)
        self.transform = Transform()
        self.text = text
        self.font = pg.font.Font('freesansbold.ttf', size)
        self.color = color
        self.textcmp =self.font.render(self.text,True,self.color)

    def start(self):
        pass

    def setText(self,text):
        self.textcmp = self.font.render(text,True,self.color)

    def update(self,dt):
        Game.get().surface.blit(self.textcmp,((int(self.parent.relativeTransform.position.x - (Camera.DX+Camera.PX)*(not self.parent.fixed) ),int(self.parent.relativeTransform.position.y- (Camera.DY+Camera.PY)*(not self.parent.fixed) )), (int(self.parent.relativeTransform.scale.x*Camera.ZX if (not self.parent.fixed) else self.parent.relativeTransform.scale.x), int(self.parent.relativeTransform.scale.y*Camera.ZY if (not self.parent.fixed) else self.parent.relativeTransform.scale.y))))
