TITLE       = "Virtual image at -2f with object at f/2"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=2.5))
    path.append(Lens(f=5))
    path.append(Space(d=10))
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()