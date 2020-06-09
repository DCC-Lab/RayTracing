import envexamples
from raytracing import *

path = ImagingPath()
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=2.5))
path.append(Space(d=10))
path.lagrangeInvariant()
print(path.lagrangeInvariant())
path.display()

