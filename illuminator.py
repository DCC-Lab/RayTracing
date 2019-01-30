from ABCD import *

path = OpticalPath()
path.name = "Kohler illumination"
path.objectHeight = 1.0
path.fanAngle = 0.5
path.rayNumber = 3
path.append(Space(d=4))
path.append(Lens(f=4,diameter=2.5))
path.append(Space(d=4+25))
path.append(Lens(f=25, diameter=7.5))
path.append(Space(d=20))
path.append(Space(d=5))
path.append(Space(d=9))
path.append(Lens(f=9, diameter=8))
path.append(Space(d=9))

print(path.fieldStop())
print(path.fieldOfView())
path.display()
