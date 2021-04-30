TITLE       = "A single lens f = 50 mm, infinite diameter"
DESCRIPTION = """
Here we have a single lens of focal length f=50 mm. An object
(in blue) is positionned at 100 mm in front of the lens. The image
conjugate (in red) is seen 100 mm after the lens, as expected.
"""
DIFFICULTY  = 1

from raytracing import *

def exempleCode():
	path = ImagingPath()
	path.label = TITLE
	path.append(Space(d=100))
	path.append(Lens(f=50))
	path.append(Space(d=100))
	path.display(comments=DESCRIPTION)

if __name__ == "__main__":
	exempleCode()