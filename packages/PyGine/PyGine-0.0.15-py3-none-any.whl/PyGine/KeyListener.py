import pygame as pg

class KeyListener :
    stroke = {}

    def getPressed(key):
        return pg.key.get_pressed()[key]

    def getPressed_Hold(key):
        return pg.key.get_pressed()[key]
    
    def getPressed_Click(key):
        if pg.key.get_pressed()[key] and not KeyListener.stroke.get(key,False):
            KeyListener.stroke[key] = True
            return True
        elif not pg.key.get_pressed()[key]:
            KeyListener.stroke[key] = False
        return False

