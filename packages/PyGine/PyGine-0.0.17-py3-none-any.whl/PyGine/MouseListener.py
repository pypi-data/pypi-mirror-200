import pygame as pg
import PyGine.Vector3 as Vector3



class MouseListener :

    def getPressed(bt):
        return pg.mouse.get_pressed(5)[bt]

    def getClicked(bt):
        global isPressed
        if pg.mouse.get_pressed(5)[bt] and not isPressed:
            isPressed = True
            return True
        elif not pg.mouse.get_pressed(5)[bt]:
            isPressed = False
        return False

    def getPos() -> Vector3:
        return Vector3.Vector3(pg.mouse.get_pos()[0],pg.mouse.get_pos()[1],0)

    def getDrag():
        return Vector3.Vector3(pg.mouse.get_rel()[0],pg.mouse.get_rel()[1],0)
