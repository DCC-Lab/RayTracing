TITLE       = "Focussing through a dielectric slab"
DESCRIPTION = """ When light focusses through a dielectric material, it is
refracted. The effect on the position of the image can be see here: the first
red arrow at z=200 mm arrow is the image that would have been obtained without
the dielectric.  However, the presence of this dielectric moves the final
image to approximately 213 mm. Because all elements have infinite diameters,
it is not possible to use the  principal ray and the axial ray because they
are not defined."""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=50))
    path.append(Space(d=30))
    path.append(DielectricSlab(n=1.5, thickness=40))
    path.append(Space(d=100))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()