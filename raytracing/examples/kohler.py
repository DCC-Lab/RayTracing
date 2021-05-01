import envexamples

from raytracing import *

'''
This code compares the same system with and without Kohler illumination. The overlay of conjugate planes can determine indeed if the light source is imaged with the sample or not, significantly reducing the quality of the images. 
'''

illumination = ImagingPath()
illumination.design(fontScale=1.5)
illumination.append(Space(d=20))
illumination.append(Lens(f=10, diameter=25.4, label="Collector"))
illumination.append(Space(d=30))
illumination.append(Aperture(diameter=2, label="Field diaphragm"))
illumination.append(Space(d=10+30))
illumination.append(Lens(f=30, diameter=25.4, label="Condenser"))
illumination.append(Space(d=30+30))
illumination.append(Lens(f=30, diameter=25.4, label="Objective"))
illumination.append(Space(d=30+30))
illumination.append(Lens(f=30, diameter=25.4, label="Tube"))
illumination.append(Space(d=30+30))
illumination.append(Lens(f=30, diameter=25.4, label="Eyepiece"))
illumination.append(Space(d=30+2))
illumination.append(Lens(f=2, diameter=10, label="Eye Entrance"))
illumination.append(Space(d=2))
illumination.display(interactive=False, raysList=[
                       LampRays(diameter=0.1, NA=0.5, N=2, T=6, z=6.6666666, rayColors='r', label="Source"),
                       ObjectRays(diameter=2, halfAngle=0.1, H=2, T=2, z=120, rayColors='g', color='g', label="Sample")], removeBlocked=False)

