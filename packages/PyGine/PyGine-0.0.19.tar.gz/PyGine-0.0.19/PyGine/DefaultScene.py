import PyGine.Scene
class DefaultScene(PyGine.Scene) :
    def __init__(self):
        super().__init__()
        self.name = "DefaultScene"

    def start(self):
        print("Start the default scene !")
