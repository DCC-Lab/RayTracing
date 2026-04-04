from raytracing import *

TITLE = "Double-Sided Telecentric"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 80.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=20))
    path.append(Lens(f=80, diameter=32))
    path.append(Space(d=80))
    path.append(Aperture(diameter=10))
    path.append(Space(d=80))
    path.append(Lens(f=80, diameter=32))
    path.append(Space(d=80))
    path.display(comments=comments)
