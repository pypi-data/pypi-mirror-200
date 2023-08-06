import math

from PyGine.CircleColliderComponent import CircleColliderComponent

from PyGine.BoxColliderComponent import BoxColliderComponent
import PyGine.Debug as Debug

class PhysicCollisionModule :
    instance = None

    def __init__(self) :
        self.CollidersList = []

    def AddCollision(self, o) :
        self.CollidersList.append(o)


    def RemoveCollision(self, o) :
        self.CollidersList.remove(o)


    def Update(self) :
        Debug.addCalculation(len(self.CollidersList)**2)
        for i in self.CollidersList :
            for j in self.CollidersList :
                if i != j :
                    self.Collide(i, j)


    def Collide(self, o1, o2) :
        #if the two objects are from the same class
            if o1.__class__ == CircleColliderComponent and o2.__class__ == CircleColliderComponent :
                self.CircleToCircle(o1,o2)
            elif o1.__class__ == CircleColliderComponent and o2.__class__ == BoxColliderComponent :
                self.CircleToBox(o1,o2)
            elif o1.__class__ == BoxColliderComponent  and o2.__class__ ==  CircleColliderComponent:
                self.CircleToBox(o2, o1)
            elif o1.__class__ == BoxColliderComponent and o2.__class__ == BoxColliderComponent :
                self.BoxToBox(o1,o2)

    def BoxToBox(self, o, i) :
        if (o.transform.position.x + o.transform.scale.x > i.transform.position.x > o.transform.position.x) or \
                (i.transform.position.x + i.transform.scale.x > o.transform.position.x > i.transform.position.x):
            if (o.transform.position.y + o.transform.scale.y > i.transform.position.y > o.transform.position.y) or \
                    (i.transform.position.y + i.transform.scale.y > o.transform.position.y > i.transform.position.y):

                i.CallCollide(o)
                o.CallCollide(i)

    def CircleToBox(self, i, o) :
        closestX = o.transform.position.x
        closestY = o.transform.position.y
        if abs(i.transform.position.x - (o.transform.position.x+o.transform.scale.x)) < abs(i.transform.position.x - closestX) :
            closestX = o.transform.position.x+o.transform.scale.x
        if abs(i.transform.position.y - (o.transform.position.y+o.transform.scale.y)) < abs(i.transform.position.y - closestY) :
            closestY = o.transform.position.y+o.transform.scale.y

        if math.sqrt((i.transform.position.x-closestX)**2 + (closestY-i.transform.position.y)**2) < i.transform.scale.x :
            i.CallCollide(o)
            o.CallCollide(i)

    def CircleToCircle(self, o1, o2) :
        if math.sqrt((o1.transform.position.x-o2.transform.position.x)**2 + (o1.transform.position.y-o2.transform.position.y)**2) < o1.transform.scale.x + o2.transform.scale.x :
            #call collision
            o1.CallCollide(o2)
            o2.CallCollide(o1)

def instance():

    if PhysicCollisionModule.instance == None :
        PhysicCollisionModule.instance = PhysicCollisionModule()
    return PhysicCollisionModule.instance