import os
import sys
sys.path.insert(0, os.path.abspath('../'))

from raytracing import *

'''
DESCRIPTION
'''

#illumination = ImagingPath()

#illumination.append(Space(d=10))
#illumination.append(Lens(f=10, diameter=100, label="Collector"))
#illumination.append(Space(d=10+30))
#illumination.append(Lens(f=30, diameter=100, label="Condenser"))
#illumination.append(Space(d=30+7))
#illumination.append(Lens(f=7, diameter=100, label="Objective"))
#illumination.append(Space(d=7+30))
#illumination.append(Lens(f=30, diameter=100, label="Tube"))
#illumination.append(Space(d=30+10))
#illumination.append(Lens(f=10, diameter=100, label="Eyepiece"))
#illumination.append(Space(d=10))
#illumination.append(Aperture(diameter=20, label="Eye entrance"))
#illumination.append(Space(d=10))

#illumination.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)

path = ImagingPath()
path.label="(a) Vignetting with FS poorly placed because of second lens diameter"
path.append(Space(d=50))
path.append(Lens(f=50, diameter=15, label="First lens"))
path.append(Space(d=100))
path.append(Lens(f=50, diameter=15, label="Second lens"))
path.append(Space(d=50))
path.append(Aperture(diameter=10, label='Camera'))
path.append(Space(d=50))

print("The Lagrange Invariant of this system is {}".format(path.lagrangeInvariant()))
path.display(limitObjectToFieldOfView=True, onlyChiefAndMarginalRays=True)