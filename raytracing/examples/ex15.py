TITLE       = "Model Olympus objective LUMPlanFL40X"
DESCRIPTION = """ Using the Objective class of Raytracing, we have used the
specifications of the LUMPlanFL40X objective to model it for use. It can be
used in any system, and it can be flipped with the flip() command if needed.
"""

from raytracing import *

def exempleCode(comments=None):
    path = ImagingPath()
    path.label = TITLE
    path.append(Space(180))
    path.append(olympus.LUMPlanFL40X())
    path.append(Space(10))
    path.displayWithObject(diameter=10, fanAngle=0.005, comments=comments)

if __name__ == "__main__":
    exempleCode()