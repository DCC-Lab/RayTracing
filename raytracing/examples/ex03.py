TITLE       = "Finite-diameter lens"
DESCRIPTION = """
An object at z=0 (front edge) is used with default properties (see Demo #1). Notice the aperture stop (AS)
identified at the lens which blocks the cone of light. There is no field stop to restrict the field of view,
which is why we must use the default object and cannot restrict the field of view. Notice how the default
rays are blocked.
"""

from raytracing import *

def exempleCode():
    path = ImagingPath()
    path.label = "Demo #3: Finite lens"
    path.append(Space(d=10))
    path.append(Lens(f=5, diameter=2.5))
    path.append(Space(d=3))
    path.append(Space(d=17))
    path.display(comments="""Demo #3: A finite lens
    An object at z=0 (front edge) is used with default properties (see Demo #1). Notice the aperture stop (AS)
    identified at the lens which blocks the cone of light. There is no field stop to restrict the field of view,
    which is why we must use the default object and cannot restrict the field of view. Notice how the default
    rays are blocked.

    path = ImagingPath()
    path.objectHeight = 1.0    # object height (full).
    path.objectPosition = 0.0  # always at z=0 for now.
    path.fanAngle = 0.5        # full fan angle for rays
    path.fanNumber = 9         # number of rays in fan
    path.rayNumber = 3         # number of points on object
    path.label = "Demo #3: Finite lens"
    path.append(Space(d=10))
    path.append(Lens(f=5, diameter=2.5))
    path.append(Space(d=3))
    path.append(Space(d=17))
    path.display()
    """)

if __name__ == "__main__":
    exempleCode()