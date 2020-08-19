import envexamples
from raytracing import *
import matplotlib.pyplot as plt
import numpy as np


"""





"""
# List of the scan angle of the ray making it throught the system. 
thetas = []

# List of 1 corresponding to the number of elements in heights 
# so that plt.plot() doesn't freak out. 
positions = []

# Radius of the laser beam at the scanning element.
# Focal spot radius (Airy disk radius)
objectHalfHeight =focalRadius= 0.000250

# Angle produced by the scanning element.
scanAngle = 10*np.pi/180

# Production of rays in the angle range of the scanning element.
scanRays = UniformRays(yMax=0, thetaMax=scanAngle, M=1, N=nRays)

# Dictionary of pinhole factors with an empty list which will subsequently contain the transmission efficiency
# for each focal spot position
pinholeModifier = {1 / 3: [], 1: [], 3: []}

# list of all relative positions from the ideal focal spot position in nm
positions = [1000, 800, 500, 300, 150, 100, 50, 25, 0, -25, -50, -100, -150, -300, -500, -800, -1000]

# Number of total rays produced by the focal spot
nRays = 100000

# Production of rays from a focal spot with a radius determined by focalRadius
inputRays = RandomUniformRays(yMax=focalRadius, yMin=-focalRadius, maxCount=nRays)

# Focal length of the objective
objFocalLength = 5

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


def illuminationPath1():

    illumination1 = ImagingPath()
    # The object in this situation is the laser beam at the scanning element. 
    illumination1.objectHeight = objectHalfHeight*2
    illumination1.rayNumber = 3
    illumination1.fanNumber = 3
    illumination1.fanAngle = 0
    illumination1.append(System4f(f1=40, f2=75, diameter1=24.5, diameter2=24.5))
    illumination1.append(System4f(f1=100, f2=100, diameter1=24.5, diameter2=24.5))
    illumination1.append(Space(d=180/40))
    illumination1.append(UISUPLAPO60XW())
    illumination1.append(Space(d=180/40))

    return illumination1


path1 = illuminationPath1()
outputRays1 = path1.traceManyThrough(scanRays)
for i in range(len(outputRays1)):
    thetas.append(scanRays[i].theta*180/np.pi)
    positions.append(outputRays1[i].y*1000)

    scanRays.displayProgress()

plt.plot(thetas,positions)
plt.xlabel('Scan angle (degrees)')
plt.ylabel('Scanning position of the focal spot (µm)')
plt.show()

