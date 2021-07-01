TITLE       = "Kohler illumination"
DESCRIPTION = """ Kohler illumination is a strategy to obtain the most uniform
illumination at the sample.  Instead of imaging the lamp filament on the
sample, one images the lamp at the back of the objective, which will then
project the Fourier transform of the illumination pattern at the object plane.
Notice that the object (the lamp) has an image at the back focal plane of the
objective. """

from raytracing import *

def exampleCode(comments=DESCRIPTION):
    fobj, dObj, f2, d2, f3, d3 = 9, 20, 200, 50, 100, 50

    path = OpticalPath()
    path.append(Space(d=f3))
    path.append(Lens(f=f3, diameter=d3))
    path.append(Space(d=f3))
    path.append(Space(d=f2))
    path.append(Lens(f=f2, diameter=d2))
    path.append(Space(d=f2))
    path.append(Space(d=fobj))
    path.append(Lens(f=fobj, diameter=dObj))
    path.append(Space(d=fobj))
    path.label = TITLE
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()