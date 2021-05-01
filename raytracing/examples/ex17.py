TITLE       = "An optical system with vendor lenses"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    # Demo #17: Vendor lenses
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
    path.display(comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()