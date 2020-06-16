import envexamples
from raytracing import *
import matplotlib.pyplot as plt

"""
........
"""

nRays = 1000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=-minHeight, maxCount=nRays)
path = ImagingPath()
path.append(Space(d=120))
path.append(Lens(f=100,diameter=20))
path.append(Space(d=175))
path.append(Lens(f=75, diameter=20))
path.append(Space(d=75))
path.append(Aperture(diameter=4, label='Camera'))
# Counts how many rays make it through the detector
outputRays = path.traceManyThroughInParallel(inputRays, progress=False)
path.display()
outputRays.display()
