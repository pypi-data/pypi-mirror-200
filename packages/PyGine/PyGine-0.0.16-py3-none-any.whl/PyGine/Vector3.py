import math
class Vector3 :
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
    
    def __truediv__(self, other):
        return Vector3(self.x / other.x, self.y / other.y, self.z / other.z)

    def divideByScalar(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def multiplyByScalar(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def normalize(self):
        return self.divideByScalar(self.magnitude())
    
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
