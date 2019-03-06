import math as m
from raytracing import *
from raytracing.thorlabs import *

path = ImagingPath()
path.label = "Demo #1: lens f = 5cm, infinite diameter"

path.append(Space(d=0.5))
path.append(Lens(f=5))
path.append(Space(d=10))
path.display()
path.displayGaussian(beam=GaussianBeam(w=1))

