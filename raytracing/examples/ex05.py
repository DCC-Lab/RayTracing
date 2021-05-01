TITLE       = "Simple microscope system"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = TITLE
    path.fanAngle = 0.1  # full fan angle for rays
    path.fanNumber = 5  # number of rays in fan
    path.rayNumber = 5  # number of points on object
    path.append(Space(d=4))
    path.append(Lens(f=4, diameter=0.8, label='Obj'))
    path.append(Space(d=4 + 18))
    path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
    path.append(Space(d=18))
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()
