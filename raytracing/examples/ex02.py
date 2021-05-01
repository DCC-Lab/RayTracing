TITLE       = "Two lenses, infinite diameters"
DESCRIPTION = """
Here we have two thin lenses with infinite diameters.
They are set up in a 4f configuration (telescope), since they are 
separated by the sum of their focal lengths.
All elements are added to an ImagingPath in the order they are traversed.
An ImagingPath assumes an object (in blue) at the front edge of the path.
You can see the image conjugate (in red) at the focal plane of the second
lens.
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=5))
    path.append(Lens(f=5))
    path.append(Space(d=20))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()