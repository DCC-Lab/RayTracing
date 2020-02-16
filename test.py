from raytracing import *

fobj = 5
f2 = 100
f3 = 200

path = ImagingPath()

path.append(Space(d=f3))
path.append(Lens(f=f3, diameter=100))
path.append(Space(d=f3))
path.append(Space(d=f2))
path.append(Lens(f=f2, diameter=50))
path.append(Space(d=f2))
path.append(Space(d=fobj))
path.append(Lens(f=fobj, diameter=5))
path.append(Space(d=fobj))
path.display(limitObjectToFieldOfView=True,
            onlyChiefAndMarginalRays=True)
