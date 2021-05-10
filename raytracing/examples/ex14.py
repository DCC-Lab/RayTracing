TITLE       = "Generic objectives"

DESCRIPTION = """ It is possible to define microscopy Objectives that will
behave similarly to real objectives (with a finite thickness, a back aperture,
etc...).  Using the specifications of an objective, one can use the Objective
class to model essentially any objective. Real objectives from manufacturers
(Olympus, Nikon) are included in the module."""

from raytracing import *

def exampleCode(comments=None):
    obj = Objective(f=10, NA=0.8, focusToFocusLength=60, backAperture=18, workingDistance=2,
                    magnification=40, fieldNumber=1.4, label="Objective")
    print("Focal distances: ", obj.focalDistances())
    print("Position of PP1 and PP2: ", obj.principalPlanePositions(z=0))
    print("Focal spots positions: ", obj.focusPositions(z=0))
    print("Distance between entrance and exit planes: ", obj.L)

    path = ImagingPath()
    path.label = "Path with generic objective"
    path.append(Space(180))
    path.append(obj)
    path.append(Space(10))
    
    path.displayWithObject(diameter=20, fanAngle=0.005, comments=comments)

if __name__ == "__main__":
    exampleCode()