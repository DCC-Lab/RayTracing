from raytracing import *

TITLE = "Finite Conjugate Objective"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 140.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Aperture(diameter=12))
    path.append(Space(d=18.0))
    path.append(ThickLens(n=1.72, R1=32.0, R2=-45.0, thickness=5.0, diameter=24))
    path.append(Space(d=6.0))
    path.append(ThickLens(n=1.67, R1=48.0, R2=-120.0, thickness=4.0, diameter=22))
    path.append(Space(d=140.0))
    path.display(comments=comments)
