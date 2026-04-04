from raytracing import *

TITLE = "New Layout"
OBJECT_THICKNESS = "Finite"   # or "Infinity"
IMAGE_THICKNESS = 100          # or "Infinity"


def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE

    # Example sequence:
    # path.append(Space(d=50))
    # path.append(Lens(f=100, diameter=25.4))
    # path.append(Space(d=100))
    # path.append(Aperture(diameter=10))
    # path.append(Space(d=100))

    path.display(comments=comments)
