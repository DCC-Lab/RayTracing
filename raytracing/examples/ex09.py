TITLE       = "Infinite telecentric 4f telescope"
DESCRIPTION = """ Two lenses separated by the sum of their focal lengths is a
telecentric telescope, or a 4f-system.  If we set up the path from the focal
plane of the first lens to the focal plane of the second lens (as is done
here), then the system has a transfer matrix that is "imaging", with B=0. This
can be checked with path.isImaging.

Raytracing defines System4f() to conveniently put two lenses
in this configuration: System4f(lens1, lens2).
"""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(Lens(f=50))
    path.append(Space(d=100))
    path.append(Lens(f=50))
    path.append(Space(d=50))
    print("Transfer matrix of system is imaging (i.e. B=0): {0}".format(path.isImaging))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()
