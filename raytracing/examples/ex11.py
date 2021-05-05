TITLE       = "Thick diverging lens"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode(comments=None):
    # Demo #11: Thick diverging lens
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(ThickLens(R1=-20, R2=20, n=1.55, thickness=10, diameter=25, label='Lens'))
    path.append(Space(d=50))
    path.displayWithObject(diameter=20, comments=comments)

if __name__ == "__main__":
    exempleCode()