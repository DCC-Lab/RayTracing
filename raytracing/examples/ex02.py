TITLE       = "Two lenses, infinite diameters"
DESCRIPTION = """ Here we have two thin lenses with infinite diameters. They
are set up in a 4f configuration (telescope), since they are  separated by the
sum of their focal lengths. All elements are added to an ImagingPath in the
order they are traversed. An ImagingPath assumes an object (in blue) at the
front edge of the path. You can see the image conjugate (in red) at the focal
plane of the second lens. """

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(Lens(f=50))
    path.append(Space(d=200))
    path.append(Lens(f=50))
    path.append(Space(d=100))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()