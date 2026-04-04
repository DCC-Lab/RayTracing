from raytracing import *

TITLE = "20x Infinity Objective + 200 mm Tube Lens"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 200.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=10.0))
    path.append(Lens(f=10, diameter=8))
    path.append(Aperture(diameter=6))
    path.append(Space(d=60.0))
    path.append(Lens(f=200, diameter=30))
    path.append(Space(d=200.0))
    path.display(comments=comments)
