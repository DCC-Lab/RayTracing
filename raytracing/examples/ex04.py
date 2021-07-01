TITLE       = "Aperture behind lens acting as Field Stop"
DESCRIPTION = """ An object at z=0 (front edge of ImagingPath) is used with
default properties. Notice the aperture stop (AS) identified at the lens which
blocks the cone of light. The second aperture, after the lens, is the Field Stop
(FS) and limits the field of view."""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=100))
    path.append(Lens(f=50, diameter=30))
    path.append(Space(d=30))
    path.append(Aperture(diameter=30))
    path.append(Space(d=170))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()