TITLE       = "Infinite telecentric 4f telescope"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=5))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.append(Lens(f=5))
    path.append(Space(d=5))
    path.display(comments=comments)

if __name__ == "__main__":
    exempleCode()
