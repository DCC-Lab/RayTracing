import envexamples
from raytracing import *

f=20
path = ImagingPath()
path.append(Space(d=f))
path.append(Lens(f=f,diameter=f))
path.append(Space(d=45))
path.append(Lens(f=25, diameter=f))
path.append(Space(d=25))
path.append(Aperture(diameter=2, label='Camera'))


nRays = 1000000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMin=minHeight, yMax=maxHeight,maxCount=nRays)
outputRays = path.traceManyThrough(inputrays)
outputRays.display(“title”)
#path.display(onlyPrincipalAndAxialRays=False, limitObjectToFieldOfView=False)


 