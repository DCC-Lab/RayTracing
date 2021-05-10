TITLE       = "Simple microscope system"
DESCRIPTION = """
This is an extremely simple microscope with ideal lenses: the objective lens
(labelled 'Obj') has a focal length of 4 mm and is positionned 184 mm from the
tube lens (f=180 mm).  You can zoom using the mouse to inspect the object.
You can see the field of view (hollow blue arrow) and the object (filled blue
arrow) at the focal plan of the objective.
"""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=4))
    path.append(Lens(f=4, diameter=8, label='Obj'))
    path.append(Space(d=4 + 180))
    path.append(Lens(f=180, diameter=50, label='Tube Lens'))
    path.append(Space(d=180))
    path.display(ObjectRays(diameter=1, halfAngle=0.5),comments=comments)

if __name__ == "__main__":
    exampleCode()
