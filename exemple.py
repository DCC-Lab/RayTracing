from ABCD import *

path = OpticalPath()
path.name = "Systeme balayage"
path.append(Space(d=0))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10, diameter=2.5))
path.append(Space(d=11))
path.append(Lens(f=1, diameter=2.5))
path.append(Space(d=1))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
