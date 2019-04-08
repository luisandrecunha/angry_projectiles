class ObjProperties:
    # Class that defines the projectile (object) properties

    # Object properties
    Cd = 0.0  # drag coefficient, [unitless], https://en.wikipedia.org/wiki/Drag_coefficient
    A  = 0.05 # reference area of the object, [meter ^ 2]
    x0 = 0.0  # initial x-position of the object, [meter]
    y0 = 0.0  # initial y-position, [meter]
    m  = 1.0  # mass of the object, [kg]
    
    def __init__(self, x0=0.0, y0=0.0, mass=1.0):
        # Main function that calls and sets the properties
        self.setProperties(x0, y0, mass)
        
    def setProperties(self, x0, y0, mass):
        # Check properties
        if y0 < 0:
            raise Exception('The initial y-position (y0) must be greater or equal to 0.')
        elif mass < 0:
            raise Exception('The mass of object must be greater or equal to 0.')

        # If no errors detected, initializes the properties
        self.x0 = x0
        self.y0 = y0
        self.m  = mass
        
    def setDragProperties(self, Cd, A):
        # Set the properties for projectiles that will have drag during their path
        if Cd < 0:
            raise Exception('The drag coefficient (Cd) must be greater or equal to 0.')
        elif A <= 0:
            raise Exception('The reference area (A) must be greater than 0.')

        # If no errors detected, initializes the properties
        self.Cd = Cd
        self.A  = A

# Different classes for each type of object that could be used as projectile
class Custom(ObjProperties):
    def __init__(self, Cd=1.0, A=0.05, x0=0.0, y0=0.0, mass=1.0):
        self.setDragProperties(Cd, A)
        self.setProperties(x0, y0, mass)

class Sphere(ObjProperties):
    def __init__(self, A=0.05, x0=0.0, y0=0.0, mass=1.0):
        self.setDragProperties(0.47, A)
        self.setProperties(x0, y0, mass)
class Cube(ObjProperties):
    def __init__(self, A=0.05, x0=0.0, y0=0.0, mass=1.0):
        self.setDragProperties(1.05, A)
        self.setProperties(x0, y0, mass)

class StreamlinedBody(ObjProperties):
    def __init__(self, A=0.04, x0=0.0, y0=0.0, mass=1.0):
        self.setDragProperties(0.04, A)
        self.setProperties(x0, y0, mass)
