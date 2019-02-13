import sys
import os
sys.path.insert(0, os.path.abspath('../'))

from raytracing import *

path = ImagingPath()
path.name = "Scanning system"
path.append(Space(d=5))
path.append(Lens(f=5, diameter=2.5))
path.append(Space(d=15))
path.append(Lens(f=10, diameter=2.5))
path.append(Space(d=11))
path.append(Lens(f=1, diameter=2.5))
path.append(Space(d=1))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
