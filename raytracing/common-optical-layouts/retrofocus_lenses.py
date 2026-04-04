from raytracing import *

TITLE = "Retrofocus Lenses"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 36.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=12.0))
    path.append(ThickLens(n=1.61, R1=-65.0, R2=34.0, thickness=7.0, diameter=44))
    path.append(Space(d=20.0))
    path.append(Aperture(diameter=18))
    path.append(Space(d=8.0))
    path.append(ThickLens(n=1.70, R1=42.0, R2=-120.0, thickness=8.0, diameter=34))
    path.append(Space(d=26.0))
    path.append(ThickLens(n=1.72, R1=58.0, R2=-44.0, thickness=6.5, diameter=30))
    path.append(Space(d=36.0))
    path.display(comments=comments)
