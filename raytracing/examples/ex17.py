TITLE       = "An optical system with vendor lenses"
DESCRIPTION = """
All vendor lenses could be used just like any other elements. Remember to 
check backFocalLength() and effectiveFocalLengths() to understand that the focal
point is not "f_e" after the lens but rather "BFL" after the lens.
"""

from raytracing import *

def exampleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(thorlabs.AC254_050_A())
    path.append(Space(d=50))
    path.append(thorlabs.AC254_050_A())
    path.append(Space(d=150))
    path.append(eo.PN_33_921())
    path.append(Space(d=50))
    path.append(eo.PN_88_593())
    path.append(Space(180))
    path.append(olympus.LUMPlanFL40X())
    path.append(Space(10))
    path.display(comments=comments)

if __name__ == "__main__":
    exampleCode()