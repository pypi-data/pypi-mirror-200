from abc import ABC


class Component() :
    def __init__(self, parent,name="") :
        self.name = name
        self.parent = parent


    def Mstart(self):
        self.earlyStart()
        self.start()

    def start(self):
        pass

    def earlyStart(self):
        pass

    def Mupdate(self,dt):
        self.update(dt)
    def update(self,dt):
        pass


    def Mend(self):
        self.end()

    def end(self):
        pass


    def onCollide(self,obj):
        pass

    def onMouseRight(self,button):
        pass

