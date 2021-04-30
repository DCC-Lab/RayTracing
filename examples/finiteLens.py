TITLE       = "Lens of f=50 mm, with finite diameter"
DESCRIPTION = """ 
A lens of focal length f=50 mm, but with a 1-inch diameter. 
Because this is set up as an ImagingPath, an object is assumed at the front of
the setup, here 100 mm before the lens. Notice the gray bars that indicate the
finite diameter of the lens. Also notice that this finite diameter does not
change the position of the conjugate plane, which is exactly where we expect
it, 100 mm after the lens."""
DIFFICULTY  = 3

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=25.4))
    path.append(Space(d=30))
    path.append(Space(d=170))
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()