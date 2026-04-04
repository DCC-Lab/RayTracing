from raytracing import *

TITLE = "4f"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 100

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=100, diameter=30))
    path.append(Space(d=100))
    path.append(Aperture(diameter=18))
    path.append(Space(d=100))
    path.append(Lens(f=100, diameter=30))
    path.append(Space(d=100))
    path.display(comments=comments)
