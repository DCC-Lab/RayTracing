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
path = ImagingPath()
path.append(System4f(f1=50, diameter1=25, f2=50, diameter2=50))
path.append(Aperture(diameter=10, label='Camera'))
outputRays = path.traceManyThrough(inputRays, progress=False)
efficiency = 100*outputRays.count/inputRays.count
path.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)

###
nRays = 100000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=minHeight, maxCount=nRays)
path = ImagingPath()
path.append(System4f(f1=50, diameter1=25, f2=50, diameter2=50))
path.append(Aperture(diameter=0.5, label='Camera'))
outputRays = path.traceManyThrough(inputRays, progress=False)
efficiency = 100*outputRays.count/inputRays.count
path.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays.display("Output profile {0:.0f}% efficiency".format(efficiency), showTheta=False)