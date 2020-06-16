import envexamples
from raytracing import *
import matplotlib.pyplot as plt

"""
........
"""

nRays = 1000000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=-minHeight, maxCount=nRays)
f=20
path = ImagingPath()
path.append(Space(d=f))
path.append(Lens(f=f,diameter=f))
path.append(Space(d=45))
path.append(Lens(f=25, diameter=f))
path.append(Space(d=25))
path.append(Aperture(diameter=2, label='Camera'))
# Counts how many rays make it through the detector
outputRays = path.traceManyThroughInParallel(inputRays, progress=False)
path.display()
outputRays.display()


 