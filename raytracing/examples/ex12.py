TITLE       = "Thick diverging lens built from individual elements"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode(comments=None):
    # Demo #12: Thick diverging lens built from individual elements
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(DielectricInterface(R=-20, n1=1.0, n2=1.55, diameter=25, label='Front'))
    path.append(Space(d=10, diameter=25, label='Lens'))
    path.append(DielectricInterface(R=20, n1=1.55, n2=1.0, diameter=25, label='Back'))
    path.append(Space(d=50))
    path.displayWithObject(diameter=20, comments=comments)


if __name__ == "__main__":
    exempleCode()