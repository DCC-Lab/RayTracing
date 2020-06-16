import envexamples
from raytracing import *
import matplotlib.pyplot as plt

"""
........
"""

nRays = 1000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=minHeight, maxCount=nRays)
path = ImagingPath()
path.append(System4f(f1=50, diameter1=25, f2=50, diameter2=50))
path.append(Aperture(diameter=20, label='Camera'))
outputRays = path.traceManyThrough(inputRays, progress=False)
efficiency = 100*outputRays.count/inputRays.count
path.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)