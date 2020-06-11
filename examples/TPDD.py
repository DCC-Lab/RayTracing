import envexamples
from raytracing import *

nRays = 1000000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMin=minHeight, yMax=maxHeight)
path = ImagingPath()
path.append(Space(d=20))
path.append(Lens(f=20,diameter=8))
path.append(Space(d=45))
path.append(Lens(f=25, diameter=8))
path.append(Space(d=25))
path.append(Aperture(diameter=2, label='Camera'))
path.display(onlyPrincipalAndAxialRays=True, limitObjectToFieldOfView=False)
 