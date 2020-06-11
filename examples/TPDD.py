import envexamples
from raytracing import *

nRays = 1000000
minHeight=-0.5
maxHeight=0.5

inputRays = RandomLambertianRays(yMin=minHeight, yMax=maxHeight)
path = ImagingPath()
path.name = "..."
path.objectHeight = 1.0
path.append(System4f(f1=50, diameter1=10, f2=50, diameter2=10))
path.append(Aperture(diameter=5, label='Camera'))
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=False)
