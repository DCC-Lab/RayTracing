try:
    from ABCD import *
    from Axicon import *
    from math import  *
except ImportError:
    raise ImportError('You must have ABCD.py installed. run "python ABCD.py install"')

f1 = 45.0
f2 = 75.0
fs = 100.0
ft = 150.0
fo = 180/40.0

class Objective(OpticalPath):
    def __init__(self, f, NA, focusToFocusLength, backAperture, workingDistance, label=''):
        self.f = f
        self.NA = NA
        self.focusToFocusLength = focusToFocusLength
        self.backAperture = backAperture
        self.workingDistance = workingDistance
        self.frontAperture = 2.0 * NA * workingDistance

        elements = [Aperture(diameter=backAperture),
                    Space(f),
                    Matrix(1,0,0,1, physicalLength=focusToFocusLength-2*f),
                    Lens(f=f),
                    Space(d=f-workingDistance),
                    Aperture(diameter=self.frontAperture),
                    Space(workingDistance)]

        super(Objective, self).__init__(elements=elements, label=label)
    
    # def pointsOfInterest(self, z):
    #     """ List of points of interest for this element as a dictionary:
    #     'z':position
    #     'label':the label to be used.  Can include LaTeX math code.
    #     """
    #     return [{'z': z, 'label': '$F_b$'}, {'z': z+self.focusToFocusLength, 'label': '$F_f$'}]

    def drawAt(self, z, axes):
        L = self.focusToFocusLength
        f = self.f
        wd = self.workingDistance
        edge = 0

        halfHeight = self.backAperture/2

        axes.add_patch(patches.Polygon(
               [[z, halfHeight],
                [z, halfHeight + edge],
                [z + L - 7*wd, halfHeight + edge],
                [z + L - wd, self.frontAperture/2],
                [z + L - wd, -self.frontAperture/2],
                [z + L - 7*wd, -halfHeight - edge],
                [z, -halfHeight - edge],
                [z, -halfHeight]],
               linewidth=1, linestyle='--',closed=True,
               color='k', fill=False))

        self.drawCardinalPoints(z, axes)
        self.elements[0].drawAperture(z, axes)
        self.elements[-2].drawAperture(z+self.focusToFocusLength-self.workingDistance, axes)

obj = Objective(f=10, NA=0.8, focusToFocusLength=60, backAperture=18, workingDistance=2, label="Objective")
print("focal dist", obj.focalDistances())
print("p1 p2", obj.principalPlanePositions(z=10))
print("f1 f2 pos", obj.focusPositions(z=10))
print("Physical length", obj.L)

path1 = OpticalPath()
path1.fanAngle = 0.0
path1.fanNumber = 1
path1.rayNumber = 15
path1.objectHeight = 10.0

path1.label = "Objective"
path1.append(Space(180))
path1.append(obj)
path1.append(Space(10))
path1.display()

path2 = OpticalPath()
path2.append(Aperture(diameter=8, label='Polygon'))
path2.append(Space(d=f1))
path2.append(Lens(f=f1, diameter=25, label='F2'))
path2.append(Space(d=f1))
path2.append(Space(d=f2))
path2.append(Lens(f=f2, diameter=25, label='F3'))
path2.append(Space(d=10))
path2.append(path1)

path2.display(limitObjectToFieldOfView=True,
                  onlyChiefAndMarginalRays=True)
