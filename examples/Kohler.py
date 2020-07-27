import envexamples

from raytracing import *

'''
DESCRIPTION
'''

illumination = ImagingPath()
illumination.append(Space(d=10))
illumination.append(Lens(f=10, diameter=100, label="Collector"))
illumination.append(Space(d=10+30))
illumination.append(Lens(f=30, diameter=100, label="Condenser"))
illumination.append(Space(d=30+30))
illumination.append(Lens(f=30, diameter=100, label="Objective"))
illumination.append(Space(d=30+30))
illumination.append(Lens(f=30, diameter=100, label="Tube"))
illumination.append(Space(d=30+30))
illumination.append(Lens(f=30, diameter=100, label="Eyepiece"))
illumination.append(Space(d=30+2))
illumination.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination.append(Space(d=2))

illumination.design(lampRayColors='y')
illumination.display(raysList=[LampRays(15, N=50),
                       ObjectRays(40, halfAngle=0, T=1, z=0, rayColors='r', color='r'),
                       ObjectRays(30, halfAngle=0, T=1, z=80, rayColors='g', color='g')], removeBlocked=False)

