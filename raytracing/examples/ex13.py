TITLE       = ""
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    M1 = Space(d=10)
    M2 = Lens(f=5)
    M3 = M2 * M1
    print(M3.forwardConjugate())
    print(M3.backwardConjugate())
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()