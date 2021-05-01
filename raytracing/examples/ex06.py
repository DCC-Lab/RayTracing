TITLE       = ""
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = "Demo #6: Simple microscope system, only principal rays"
    path.append(Space(d=4))
    path.append(Lens(f=4, diameter=0.8, label='Obj'))
    path.append(Space(d=4 + 18))
    path.append(Lens(f=18, diameter=5.0, label='Tube Lens'))
    path.append(Space(d=18))
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()