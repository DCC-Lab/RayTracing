TITLE       = "Laser beam and vendor lenses"
DESCRIPTION = """
It is possible to propagate gaussian beams using a LaserPath instead of an imaging
path.  The formalism makes use of the same matrices, but the GaussianBeam is
different from a ray: it is a complex radius of curvature (q), but all the complexity
is hidden in the GaussianBeam class (although you can access q, w, zo, etc..).
Note that any diffraction of the beam from edges of element is not considered
because the formalism does not allow it: a gaussian beam remains a gaussian beam
and therefore will not be clipped by lenses.
"""

from raytracing import *

def exampleCode(comments=None):
    # Demo #18: Laser beam and vendor lenses
    path = LaserPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(thorlabs.AC254_050_A())
    path.append(Space(d=50))
    path.append(thorlabs.AC254_050_A())
    path.append(Space(d=150))
    path.append(eo.PN_33_921())
    path.append(Space(d=50))
    path.append(eo.PN_88_593())
    path.append(Space(d=180))
    path.append(olympus.LUMPlanFL40X())
    path.append(Space(d=10))
    path.display(beams=[GaussianBeam(w=0.001)], comments=comments)

if __name__ == "__main__":
    exampleCode()