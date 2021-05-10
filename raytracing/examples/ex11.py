TITLE       = "Thick diverging lens computed from the Lensmaker equation"
DESCRIPTION = """ Raytracing offers a simple "thick lens" that has a non-null
thickness.  You need to provide R1 and R2 as well as the index and the
thickness of the lens. It computes a single transfer matrix based on the
application of a dielectric, space and dielectric transfer matrix. Notice
that, in line with the paraxial approximation, the vertex is where the
curvature of the rays occur, even if in this case the curvature brings the
surface away from the vertex. Blocking of rays inside the lens is not
calculated: you would need to build a MatrixGroup with all elements to do so
(and this is what CompoundLens and AchromaticDoublets do)."""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
    path.append(Space(d=50))
    path.displayWithObject(diameter=20, comments=comments)

if __name__ == "__main__":
    exampleCode()