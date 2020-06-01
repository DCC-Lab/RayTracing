import envexamples

from raytracing import *

'''
DESCRIPTION
'''

# Source with Kohler illumination 
illumination1 = ImagingPath()
illumination1.fanNumber = 1
illumination1.fanAngle = 5

illumination1.append(Space(d=10))
illumination1.append(Lens(f=10, diameter=100, label="Collector"))
illumination1.append(Space(d=10+30))
illumination1.append(Lens(f=30, diameter=100, label="Condenser"))
illumination1.append(Space(d=30+30))
illumination1.append(Lens(f=30, diameter=100, label="Objective"))
illumination1.append(Space(d=30+30))
illumination1.append(Lens(f=30, diameter=100, label="Tube"))
illumination1.append(Space(d=30+30))
illumination1.append(Lens(f=30, diameter=100, label="Eyepiece"))
illumination1.append(Space(d=30+2))
illumination1.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination1.append(Space(d=2))

print("The Lagrange Invariant of this system is {}".format(illumination1.lagrangeInvariant()))
illumination1.display()


# Sample imaging path 
illumination2 = ImagingPath()
illumination2.objectPosition = 140
illumination2.objectHeight = 5
illumination2.fanNumber = 1
illumination2.fanAngle = 0

illumination2.append(Space(d=10))
illumination2.append(Lens(f=10, diameter=100, label="Collector"))
illumination2.append(Space(d=10+30))
illumination2.append(Lens(f=30, diameter=100, label="Condenser"))
illumination2.append(Space(d=30+30))
illumination2.append(Lens(f=30, diameter=100, label="Objective"))
illumination2.append(Space(d=30+30))
illumination2.append(Lens(f=30, diameter=100, label="Tube"))
illumination2.append(Space(d=30+30))
illumination2.append(Lens(f=30, diameter=100, label="Eyepiece"))
illumination2.append(Space(d=30+2))
illumination2.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination2.append(Space(d=2))

illumination2.display()