import envexamples
from raytracing import *

path = ImagingPath()
nRays = 1000000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMin=minHeight, yMax=maxHeight)
path.name = "..."
path.append(System4f(f1=50, diameter1=10, f2=50, diameter2=10))
path.append(Aperture(diameter=5, label='Camera'))
path.display(onlyPrincipalAndAxialRays=True, limitObjectToFieldOfView=False)
