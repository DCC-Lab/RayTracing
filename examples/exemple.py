import envexamples
from raytracing import *

path = ImagingPath()
path.name = "Telescope"
path.append(Space(d=50))
path.append(Lens(f=50,diameter=25))
path.append(Space(d=50))
path.append(Space(d=100))
path.append(Lens(f=100,diameter=25))
path.append(Space(d=100))
path.display()
