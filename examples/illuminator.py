import sys
import os
sys.path.insert(0, os.path.abspath('../'))

from raytracing import *

path = ImagingPath()
path.name = "Kohler illumination with 1 cm wide lamp and 0.5 NA"
path.objectHeight = 1.0
path.fanAngle = 0.5
path.rayNumber = 3
path.append(Space(d=4))
path.append(Lens(f=4,diameter=2.5, label='Collector'))
path.append(Space(d=4+25))
path.append(Lens(f=25, diameter=7.5, label='Condenser'))
path.append(Space(d=20))
path.append(Space(d=5))
path.append(Space(d=9))
path.append(Lens(f=9, diameter=8, label='Objective'))
path.append(Space(d=9))
path.showLabels=True
print(path.fieldStop())
print(path.fieldOfView())
path.display(onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)
path.save("Illumination.png",onlyChiefAndMarginalRays=True, limitObjectToFieldOfView=True)