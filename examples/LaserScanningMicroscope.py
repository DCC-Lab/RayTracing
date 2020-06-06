import envexamples
from raytracing import *

# A polygonal mirror with 36 facets has an angle of 10 degrees, 0.1750 rad, between the facets.

class LUMPlanFL40X(Objective):

    def __init__(self):
        super(LUMPlanFL40X, self).__init__(f=180/40,
                                         NA=0.8,
                                         focusToFocusLength=40,
                                         backAperture=7,
                                         workingDistance=2,
                                         label='LUMPlanFL40X Objective',
                                         url="https://www.edmundoptics.com/p/olympus-lumplfln-40xw-objective/3901/")


illumination = ImagingPath()
# Let's say that the laser has a diameter of 500 nm.
illumination.objectHeight = 0.0005
illumination.rayNumber = 3
illumination.fanNumber = 3
illumination.fanAngle = 0
illumination.append(System4f(f1=40, f2=75, diameter1=24.5, diameter2=24.5))
illumination.append(System4f(f1=100, f2=100, diameter1=24.5, diameter2=24.5))
illumination.append(Space(d=180/40))
illumination.append(LUMPlanFL40X())
illumination.append(Space(d=180/40))
illumination.display()