import envexamples
from raytracing import *
import matplotlib.pyplot as plt


"""

DESCRIPTION EVENTUALLY WE ARE GOING TO DO THAT BUT I'M HUNGRY NOW

Mainly, it's the example 3 of assignment 2 in Biomed Imaging. 
System = Scanning microscope
Trying to prove that it makes a line at the sample by using a polygon to change the angle of the laser beam + show the size of the covered FOV. 
A polygonal mirror with 36 facets has an angle of 10 degrees, 0.1750 rad, between the facets, so scanAngle = 0.1750. 

"""

# List of the height of the ray making it throught the system. 
heights = []

# List of 1 corresponding to the number of elements in heights so that plt.plot() doesn't freak out. 
positions = []

# Radius of the laser beam at the scanning element.
objectHalfHeight = 0.000250

# Angle produced by the scanning element.
scanAngle = 0.1750

# Number of total rays considered in these calculations. 
nRays = 10000

# Production of rays in the angle range of the scanning element.
inputRays = RandomUniformRays(yMin = -objectHalfHeight, yMax = objectHalfHeight, thetaMin = -scanAngle, thetaMax = scanAngle, maxCount = nRays)


class LUMPlanFL40X(Objective):

    def __init__(self):
        super(LUMPlanFL40X, self).__init__(f=180/40,
                                         NA=0.8,
                                         focusToFocusLength=40,
                                         backAperture=7,
                                         workingDistance=2,
                                         label='LUMPlanFL40X Objective',
                                         url="https://www.edmundoptics.com/p/olympus-lumplfln-40xw-objective/3901/")


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
	illumination.append(LUMPlanFL40X())
	illumination.append(Space(d=180/40))

	return illumination



for ray in inputRays:

	rayInPath = illuminationPath().traceThrough(ray)

	if rayInPath.isNotBlocked:
		heights.append(rayInPath.y*0.000001)
		positions.append(1)

	inputRays.displayProgress()

plt.plot(heights, positions)
plt.xlabel('Scanning positions of the focal spot')
plt.show()


















