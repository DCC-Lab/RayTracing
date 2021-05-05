TITLE       = "Obtained the forward and backward conjugates"
DESCRIPTION = """
This example does not show a plot, it calculates the position
of the object and images.
"""

from raytracing import *

def exempleCode(comments=None):
    M1 = Space(d=10)
    M2 = Lens(f=5)
    M3 = M2 * M1
    print(M3.forwardConjugate())
    print(M3.backwardConjugate())

if __name__ == "__main__":
    exempleCode()