TITLE       = "Finite-diameter lens"
DESCRIPTION = """ An object at z=0 (front edge) is used with default
properties. Notice the aperture stop (AS) identified at the lens which blocks
the cone of light from the point on the axis. There is no field stop to
restrict the field of view, which is why we must use the default object and
cannot restrict the display to the field of view."""

from raytracing import *

def exempleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=25))
    path.append(Space(d=150))
    path.display(comments=comments)

if __name__ == "__main__":
    exempleCode()