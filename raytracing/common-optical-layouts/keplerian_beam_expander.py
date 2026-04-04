from raytracing import *

TITLE = "Keplerian Beam Expander"
OBJECT_THICKNESS = "Infinity"
IMAGE_THICKNESS = "Infinity"

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Aperture(diameter=12))
    path.append(Space(d=40))
    path.append(Lens(f=40, diameter=20))
    path.append(Space(d=40))
    path.append(Aperture(diameter=10))
    path.append(Space(d=120))
    path.append(Lens(f=120, diameter=42))
    path.display(comments=comments)
