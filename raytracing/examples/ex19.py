TITLE       = "Cavity round trip and calculated laser modes"
DESCRIPTION = """
Although less developed in the raytracing module, it is also possible to calculate
eigenmodes of laser cavities.
"""

from raytracing import *

def exampleCode(comments=None):
    cavity = LaserCavity(label="")
    cavity.append(Space(d=160))
    cavity.append(DielectricSlab(thickness=100, n=1.8))
    cavity.append(Space(d=160))
    cavity.append(CurvedMirror(R=-400))
    cavity.append(Space(d=160))
    cavity.append(DielectricSlab(thickness=100, n=1.8))
    cavity.append(Space(d=160))

    # Calculate all self-replicating modes (i.e. eigenmodes)
    (q1, q2) = cavity.eigenModes()
    print(q1,q2)

    # Obtain all physical modes (i.e. only finite eigenmodes)
    qs = cavity.laserModes()
    for q in qs:
        print(q)

    cavity.display(comments=comments)

if __name__ == "__main__":
    exampleCode()