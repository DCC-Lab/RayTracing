from raytracing import *

TITLE = "2f"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 200

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Aperture(diameter=25.4))
    path.append(Space(d=200))
    path.append(Lens(f=100, diameter=25.4))
    path.append(Space(d=200))
    path.display(comments=comments)
