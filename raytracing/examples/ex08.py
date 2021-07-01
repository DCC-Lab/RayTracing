TITLE       = "Virtual image at -f with object at f/2"
DESCRIPTION = """
With an object midway between the focus and the lens, we obtain a virtual
image at the front focal plane (d=-f to the left of the lens).
The exact position can be obtained with path.forwardConjugate(), which
will return the distance (from the end of the path) and the transfer matrix
to that point. That transfer marix is necessarily an imaging matrix (B=0).
"""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=25))
    path.append(Lens(f=50))
    path.append(Space(d=50))
    distance, transferMatrix = path.forwardConjugate()
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()