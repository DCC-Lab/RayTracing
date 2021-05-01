TITLE       = "Infinite telecentric 4f telescope"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=5))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=5))
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()
