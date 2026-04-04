from raytracing import *

TITLE = "Telephoto (Infinity Focus)"
OBJECT_THICKNESS = "Infinity"
IMAGE_THICKNESS = 12.0

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=20.0))
    path.append(ThickLens(n=1.69, R1=140.0, R2=-80.0, thickness=8.0, diameter=42))
    path.append(Space(d=8.0))
    path.append(Aperture(diameter=20))
    path.append(Space(d=55.0))
    path.append(ThickLens(n=1.72, R1=-35.0, R2=140.0, thickness=4.0, diameter=26))
    path.append(Space(d=12.0))
    path.display(comments=comments)
