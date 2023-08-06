from PyGine import PhysicCollisionModule

from PyGine.Component import Component


class ColliderComponent(Component):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.transform = parent.transform
        PhysicCollisionModule.instance().AddCollision(self)

    def end(self):
        PhysicCollisionModule.instance().RemoveCollision(self)

    def callCollide(self, o):
        pass
