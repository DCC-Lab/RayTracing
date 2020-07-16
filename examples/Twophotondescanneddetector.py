import envexamples
from raytracing import *
import matplotlib.pyplot as plt

"""
The emitted light in some optical systems, like two-photon descanned detector, is scattered in all directions.
The size of the diffused light dictates which lenses and detector size to choose.
Therefore,  it is of great importance to find a well-sized detector that fits the optical system.  
"""

nRays = 100000
minHeight=-0.5
maxHeight=0.5
inputRays = RandomLambertianRays(yMax=maxHeight, yMin=minHeight, maxCount=nRays)


###
path1=ImagingPath()
path1.append(System4f(f1=75,d1=50,f2=75,d2=75))
path1.append(Aperture(diameter=0.5, label='Camera'))
outputRays1 = path1.traceManyThrough(inputRays, progress=False)
efficiency1 = 100*outputRays1.count/inputRays.count
path1.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays1.display("Output profile {0:.0f}% efficiency".format(efficiency1), showTheta=False)
print(efficiency1)

###
###
path2=ImagingPath()
path2.append(System4f(f1=50,d1=25,f2=50,d2=50))
path2.append(Aperture(diameter=0.5, label='Camera'))
outputRays2 = path2.traceManyThrough(inputRays, progress=False)
efficiency2 = 100*outputRays2.count/inputRays.count
path2.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays2.display("Output profile {0:.0f}% efficiency".format(efficiency2), showTheta=False)
print(efficiency2)

###
###
path3=ImagingPath()
path3.append(System4f(f1=50,d1=25,f2=50,d2=50))
path3.append(Aperture(diameter=1, label='Camera'))
outputRays3 = path3.traceManyThrough(inputRays, progress=False)
efficiency3 = 100*outputRays3.count/inputRays.count
path3.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays3.display("Output profile {0:.0f}% efficiency".format(efficiency3), showTheta=False)
print(efficiency3)