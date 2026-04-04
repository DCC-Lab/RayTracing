from raytracing import *

TITLE = "Object-Space Telecentric"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 120.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=20))
    path.append(Lens(f=80, diameter=32))
    path.append(Space(d=80))
    path.append(Aperture(diameter=12))
    path.append(Space(d=70))
    path.append(Lens(f=120, diameter=34))
    path.append(Space(d=120))
    path.display(comments=comments)
