TITLE       = "GRIN lens"
DESCRIPTION = """
A GRIN lens is available.  It has a quadratic index of refraction and is defined
either with its alpha parameter or its pitch (it is easier to work with the pitch).
Here, we have a GRIN available from Thorlabs G1P10.  Please note that the GRIN
is not assumed to be in any medium.  Therefore, if you wish to use it in air or water
(or both at either end), you need to explicitly add a DielectricInterface with the
appropriate indices.
"""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()

    n0 = 1.66
    path.append(Space(d=0.2))
    # Dry side on the objective side (index is 1.0)
    path.append(DielectricInterface(n1=1, n2=n0, diameter=1))
    path.append(GRIN(L=3.758, n0=n0, pitch=0.433, diameter=1))
    # Water immersion side on the sample side (index is 1.33)
    path.append(DielectricInterface(n1=n0, n2=1.33, diameter=1))
    path.append(Space(d=0.2))
    path.displayWithObject(diameter=0.5, comments=comments)

if __name__ == "__main__":
    exampleCode()