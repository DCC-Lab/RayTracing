TITLE       = "Cavity round trip and calculated laser modes"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
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

    # Show
    cavity.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()