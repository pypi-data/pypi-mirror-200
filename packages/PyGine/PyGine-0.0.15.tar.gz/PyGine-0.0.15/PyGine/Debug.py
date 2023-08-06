class Debug :
    debug = False
    ShowCollidersBox = False
    calculation = 0

def resetCalculation() :
    Debug.calculation = 0

def addCalculation(n) :
    Debug.calculation += n

def PrintDebug(string:str) :
    print("Debug : "+string)
