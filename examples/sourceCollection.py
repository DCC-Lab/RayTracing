import envexamples
from raytracing import *

path = ImagingPath(label="Original setup")
path.append(Space(d=100))
path.append(Lens(f=35,diameter=25))
path.append(Space(d=35))
path.append(Aperture(diameter=0.2))
path.displayWithObject(diameter=1, removeBlocked=False)
path.reportEfficiency(objectDiameter=1, emissionHalfAngle=1.57)

path2 = ImagingPath(label="Better system imaging the emission spot on detector")
path2.append(Space(d=70))
path2.append(Lens(f=35,diameter=25))
path2.append(Space(d=70))
path2.append(Aperture(diameter=0.2))
path2.displayWithObject(diameter=1, removeBlocked=False)
path2.reportEfficiency(objectDiameter=1, emissionHalfAngle=1.57)

path3 = ImagingPath(label="Best system and larger NA imaging spot on detector")
path3.objectHeight=1
path3.append(System4f(f1=35, diameter1=25, f2=35, diameter2=35))
path3.append(Aperture(diameter=0.2))
path3.displayWithObject(diameter=1, removeBlocked=False)
#path3.reportEfficiency(objectDiameter=1, emissionHalfAngle=1.57)
