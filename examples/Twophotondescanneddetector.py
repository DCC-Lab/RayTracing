import envexamples
from raytracing import *
import matplotlib.pyplot as plt

"""
The emitted light in the some optical systems like Two photon descanned detector is scattered in all directions.
And the size of the diffused light dictates certain detectionlenses and detector size.  
Therefore,  it is of great importance to find a well-sized detector that fits in the optical system.  
"""

#How to optimize the detector size ?

nRays = 100000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=minHeight, maxCount=nRays)
path1 = ImagingPath()
path1.append(System4f(f1=25, diameter1=25, f2=50, diameter2=50))
path1.append(Aperture(diameter=0.5, label='Camera'))
outputRays = path1.traceManyThrough(inputRays, progress=False)
efficiency = 100*outputRays.count/inputRays.count
path1.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)
print(efficiency)

###
nRays = 100000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=minHeight, maxCount=nRays)
path2 = ImagingPath()
path2.append(System4f(f1=75, diameter1=75, f2=100, diameter2=100))
path2.append(Aperture(diameter=0.5, label='Camera'))
outputRays = path2.traceManyThrough(inputRays, progress=False)
efficiency = 100*outputRays.count/inputRays.count
path2.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)
print(efficiency)

###
nRays = 100000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=minHeight, maxCount=nRays)
path3 = ImagingPath()
path3.append(System4f(f1=75, diameter1=75, f2=100, diameter2=100))
path3.append(Aperture(diameter=2, label='Camera'))
outputRays = path3.traceManyThrough(inputRays, progress=False)
efficiency = 100*outputRays.count/inputRays.count
path3.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)
print(efficiency)