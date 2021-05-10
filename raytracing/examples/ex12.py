TITLE       = "Thick diverging lens built from individual elements"
DESCRIPTION = """ If you build a lens from individual elements
(DielectricInterface, Space and  DielectrcInterface), then the rays inside the
lens may be blocked from the finite diameter (in this case, Space() has a
finite diameter of 25 mm).  The drawing on the graph is not as elegant, but
the physics is more correct.  Notice the upward rays from the green point is
actually blocked inside.  However, notice that again the rays are refracting
at the vertex, in accord with the paraxial approximation. """

from raytracing import *

def exampleCode(comments=None):
    # Demo #12: Thick diverging lens built from individual elements
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(DielectricInterface(R=-20, n1=1.0, n2=1.55, diameter=25, label='Front'))
    path.append(Space(d=10, diameter=25, label='Lens'))
    path.append(DielectricInterface(R=20, n1=1.55, n2=1.0, diameter=25, label='Back'))
    path.append(Space(d=50))
    path.displayWithObject(diameter=20, comments=comments)


if __name__ == "__main__":
    exampleCode()