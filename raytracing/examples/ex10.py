TITLE       = "Retrofocus $f_e$={0:.1f} cm, and BFL={1:.1f}"
DESCRIPTION = """ A retrofocus is a system of lenses organized in such a way
that the effective focal length is shorter than the back focal length (i.e.
the distance between the surface of the lens and the focal spot). It consists
of a diverging lens followed by a converging lens. This is used to obtain a
short focal length in situations where distances are constrained. """

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.append(Space(d=20))
    path.append(Lens(f=-10, label='Div'))
    path.append(Space(d=7))
    path.append(Lens(f=10, label='Foc'))
    path.append(Space(d=40))
    (focal, focal) = path.effectiveFocalLengths()
    bfl = path.backFocalLength()
    path.label = TITLE.format(focal, bfl)
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()