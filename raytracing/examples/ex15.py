TITLE       = "Path with LUMPlanFL40X"
DESCRIPTION = """
"""

from raytracing import *

def exempleCode():
    # Demo #15: Olympus objective LUMPlanFL40X
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(180))
    path.append(olympus.LUMPlanFL40X())
    path.append(Space(10))
    path.displayWithObject(diameter=10, fanAngle=0.005, comments=DESCRIPTION)

if __name__ == "__main__":
    exempleCode()