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

# Defines the path. d1 and d2 are the diameter of the lenses, fl1 and fl2 are the focal lengths and d3 is the diameter of the aperture.
def imagingPath(fl1=10, d1=10, fl2=10, d2=10, d3=10, title=""):
    
    path = ImagingPath()
    path.label=title
    path.append(System4f(f1=fl1, diameter1=d1, f2=fl2, diameter2=d2))
    path.append(Aperture(diameter=d3, label='Camera'))
    
    return path

# Three paths with different sets of lens and aperture.

###
path1 = imagingPath(fl1=75, fl2=75, d1=50, d2=75, d3=0.5, title="")
outputRays1 = path1.traceManyThrough(inputRays, progress=False)
efficiency1 = 100*outputRays1.count/inputRays.count
path1.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays1.display("Output profile {0:.0f}% efficiency".format(efficiency1), showTheta=False)
print(efficiency1)

###
path2 = imagingPath(fl1=50, fl2=50, d1=25, d2=50, d3=0.5, title="")
outputRays2 = path2.traceManyThrough(inputRays, progress=False)
efficiency2 = 100*outputRays2.count/inputRays.count
path2.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays2.display("Output profile {0:.0f}% efficiency".format(efficiency2), showTheta=False)
print(efficiency2)

###
path3 = imagingPath(fl1=50, fl2=50, d1=25, d2=50, d3=1, title="")
outputRays3 = path3.traceManyThrough(inputRays, progress=False)
efficiency3 = 100*outputRays3.count/inputRays.count
path3.display(limitObjectToFieldOfView=False, onlyPrincipalAndAxialRays=True)
outputRays3.display("Output profile {0:.0f}% efficiency".format(efficiency3), showTheta=False)
print(efficiency3)
