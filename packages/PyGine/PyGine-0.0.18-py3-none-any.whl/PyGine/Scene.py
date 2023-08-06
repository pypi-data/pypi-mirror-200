from abc import ABC


class Scene(ABC):
    def __init__(self):
        self.GameObjects = []
        self.toBeRemoved = []
        self.Used = False

    def earlyStart(self):
        pass

    def Mstart(self):
        self.earlyStart()
        for go in self.GameObjects:
            go.Mstart()
        self.Used = True
        self.start()

    def Mupdate(self, dt):
        self.update(dt)
        for i in range(len(self.GameObjects)):
            self.GameObjects[i].Mupdate(dt)
        if (len(self.toBeRemoved) > 0):
            self.rm()

    def Mend(self):
        self.end()
        self.toBeRemoved.extend(self.GameObjects)

    def start(self):
        pass

    def update(self, dt):
        pass

    def addGameObject(self, gameObject):
        if self.Used:
            gameObject.Mstart()
        self.GameObjects.append(gameObject)
        return gameObject

    def rm(self):
        for go in self.toBeRemoved:
            if go in self.GameObjects:
                go.Mend()
                self.GameObjects.remove(go)
        self.toBeRemoved.clear()

    def end(self):
        pass

    def getGameObject(self, name):
        for el in self.GameObjects:
            if el.name == name:
                return el

    def removeGameObject(self, gameObject):
        self.toBeRemoved.append(gameObject)
