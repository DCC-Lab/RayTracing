from raytracing import *

TITLE = "Cooke Triplet"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 38.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=7.5))
    path.append(ThickLens(n=1.69, R1=38.0, R2=150.0, thickness=6.0, diameter=34))
    path.append(Space(d=4.0))
    path.append(ThickLens(n=1.67, R1=-28.0, R2=24.0, thickness=2.5, diameter=20))
    path.append(Space(d=10.0))
    path.append(Aperture(diameter=11))
    path.append(Space(d=32.0))
    path.append(ThickLens(n=1.72, R1=65.0, R2=-32.0, thickness=6.5, diameter=30))
    path.append(Space(d=38.0))
    path.display(comments=comments)
