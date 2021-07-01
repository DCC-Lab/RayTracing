TITLE       = "Finite-diameter lens"
DESCRIPTION = """ An object at z=0 (front edge) is always present in
ImagingPath. Notice the aperture stop (AS) identified at the lens which blocks
the cone of light from the point of the object on the axis. There is no field
stop to restrict the field of view, which is why we must use the default
object and why we cannot restrict the display to the field of view.
Notice the presence of an Aperture Stop (AS) but no Field Stop (FS)."""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=25))
    path.append(Space(d=150))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()