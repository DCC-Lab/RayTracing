from raytracing import *

TITLE = "Galilean Beam Expander"
OBJECT_THICKNESS = "Infinity"
IMAGE_THICKNESS = "Infinity"

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Aperture(diameter=8))
    path.append(Space(d=25))
    path.append(Lens(f=-25, diameter=14))
    path.append(Space(d=75))
    path.append(Lens(f=100, diameter=40))
    path.display(comments=comments)
