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
    def __init__(self, f, length, backAperture, workingDistance, label=''):
        elements = [Aperture(diameter=backAperture),
                    Space(f),
                    Matrix(1,0,0,1, physicalLength=length),
                    Lens(f=f),
                    Space(f)]

        super(Objective, self).__init__(elements=elements, label=label)
    
    def drawAt(self, z, axes):
        halfHeight = self.displayHalfHeight()
        p = patches.Rectangle((z, -halfHeight), self.L,
                              2 * halfHeight, color='k', fill=False,
                              transform=axes.transData, clip_on=True)
        axes.add_patch(p)


obj = Objective(f=10, length=60, backAperture=20, workingDistance=2)

path1 = OpticalPath()
path1.label = "Objective"
path1.append(Space(10))
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
