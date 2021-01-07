import envexamples
from raytracing import *
import matplotlib.pyplot as plt
import numpy as np


"""
In a laser scanning system, the scanning components define 
the covered field-of-view (FOV) at the sample plane. Here, 
we show a one-dimensional example with a polygonal mirror
of 36 facets that rotates rapidly to scan
the beam along the horizontal direction. It produces a meachnical 
sweep of 10 degrees, or 0.1750 rad, between each facets. 
Therefore, the laser beam covers a total optical scan angle of 20 degrees.
In the following example, the object is considered to be the
laser beam at the polygonal mirror plane. 
The output profile shows on its x-axis the width of the FOV under the objective. 
"""

# List of the scan angle of the ray making it throught the system. 
thetas = []

# List of 1 corresponding to the number of elements in heights 
# so that plt.plot() doesn't freak out. 
positions = []

# Radius of the laser beam at the scanning element.
objectHalfHeight = 0.000250

# Angle produced by the scanning element.
scanAngle = 10*np.pi/180

# Number of total rays considered in these calculations. 
nRays = 10000

# Production of rays in the angle range of the scanning element.
scanRays = UniformRays(yMax=0, thetaMax=scanAngle, M=1, N=nRays)

class UISUPLAPO60XW(Objective):

    def __init__(self):
        super(UISUPLAPO60XW, self).__init__(f=180/60,
                                         NA=1.2,
                                         focusToFocusLength=40,
                                         backAperture=7,
                                         workingDistance=0.28,
                                         magnification=60,
                                         fieldNumber=22,
                                         label='UISUPLAPO60XW Objective')


def illuminationPath():

    illumination = ImagingPath()
    # The object in this situation is the laser beam at the scanning element. 
    illumination.objectHeight = objectHalfHeight*2
    illumination.rayNumber = 3
    illumination.fanNumber = 3
    illumination.fanAngle = 0
    illumination.append(System4f(f1=40, f2=75, diameter1=24.5, diameter2=24.5))
    illumination.append(System4f(f1=100, f2=100, diameter1=24.5, diameter2=24.5))
    illumination.append(Space(d=180/40))
    illumination.append(UISUPLAPO60XW())
    illumination.append(Space(d=180/40))

    return illumination


path = illuminationPath()
outputRays = path.traceManyThrough(scanRays)
for i in range(len(outputRays)):
    thetas.append(scanRays[i].theta*180/np.pi)
    positions.append(outputRays[i].y*1000)

    scanRays.displayProgress()

plt.plot(thetas,positions)
plt.xlabel('Scan angle (degrees)')
plt.ylabel('Scanning position of the focal spot (µm)')
plt.show()















