from raytracing import *
from raytracing.thorlabs import *

path = LaserPath()
path.label = "Test"
path.append(Space(d=10))
path.append(Lens(f=50))
path.append(Space(d=20))
path.append(Lens(f=50))
path.append(Space(d=20))
path.display(inputBeam=GaussianBeam(w=0.03))

path2 = path.asImagingPath()
path2.display()
