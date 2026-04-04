from raytracing import *

TITLE = "Double Gauss Lens"
OBJECT_THICKNESS = "Finite"
IMAGE_THICKNESS = 48.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=8.0))
    path.append(ThickLens(n=1.67, R1=55.0, R2=180.0, thickness=7.0, diameter=40))
    path.append(Space(d=4.0))
    path.append(ThickLens(n=1.62, R1=-42.0, R2=28.0, thickness=3.0, diameter=28))
    path.append(Space(d=10.0))
    path.append(Aperture(diameter=18))
    path.append(Space(d=4.0))
    path.append(ThickLens(n=1.62, R1=28.0, R2=-42.0, thickness=3.0, diameter=28))
    path.append(Space(d=28.0))
    path.append(ThickLens(n=1.67, R1=180.0, R2=-55.0, thickness=7.0, diameter=40))
    path.append(Space(d=48.0))
    path.display(comments=comments)
