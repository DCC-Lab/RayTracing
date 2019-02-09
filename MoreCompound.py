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


path1 = OpticalPath()
path1.append(Aperture(diameter=8, label='Polygon'))
path1.append(Space(d=f1))
path1.append(Lens(f=f1, diameter=25, label='F1'))
path1.append(Space(d=f1))
path1.display(limitObjectToFieldOfView=True,
                  onlyChiefAndMarginalRays=True)

path2 = OpticalPath()
path2.append(Aperture(diameter=8, label='Polygon'))
path2.append(Space(d=f1))
path2.append(Lens(f=f1, diameter=25, label='F2'))
path2.append(Space(d=f1))
path2.append(Space(d=f2))
path2.append(Lens(f=f2, diameter=25, label='F3'))
path2.append(path1)

path2.display(limitObjectToFieldOfView=True,
                  onlyChiefAndMarginalRays=True)
