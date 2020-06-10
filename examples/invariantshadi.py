import envexamples
from raytracing import *


path = ImagingPath()
path.objectHeight = 2.5
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10,diameter=2.5))
path.append(Space(d=10))
path.lagrangeInvariant()
print(path.lagrangeInvariant())
path.display()

path1 = ImagingPath()
path1.append(Space(d=5))
path1.append(Lens(f=5, diameter=2.5))
path1.append(Space(d=15))
path1.append(Lens(f=10,diameter=2.5))
path1.append(Space(d=10))
path1.lagrangeInvariant()
print(path1.lagrangeInvariant())
path1.display()


path2 = ImagingPath()
path2.append(Space(d=5))
path2.append(Lens(f=5, diameter=1))
path2.append(Space(d=15))
path2.append(Lens(f=10,diameter=1))
path2.append(Space(d=10))
path2.lagrangeInvariant()
print(path2.lagrangeInvariant())
path2.display()


path3 = ImagingPath()
path3.append(Space(d=5))
path3.append(Lens(f=5, diameter=0.5))
path3.append(Space(d=15))
path3.append(Lens(f=10,diameter=0.5))
path3.append(Space(d=10))
path3.lagrangeInvariant()
print(path3.lagrangeInvariant())
path3.display()


