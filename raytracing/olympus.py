from .abcd import *
from .lens import *

class LUMPlanFL40X(Objective):
    """ Olympus 40x immersion objective

    Immersion not considered at this point.
    """

    def __init__(self):
        super(LUMPlanFL40X, self).__init__(f=180/40,
                                         NA=0.8,
                                         focusToFocusLength=40,
                                         backAperture=7,
                                         workingDistance=2,
                                         label='LUMPLFL40X',
                                         url="https://www.edmundoptics.com/p/olympus-lumplfln-40xw-objective/3901/")

class XLUMPlanFLN20X(Objective):
    """ Olympus XLUMPlanFLN20X (Super 20X) 1.0 NA with large 
    back aperture.

    Immersion not considered at this point.
    """
    def __init__(self):
        super(XLUMPlanFLN20X, self).__init__(f=180/20,
                                         NA=1.0,
                                         focusToFocusLength=80,
                                         backAperture=22,
                                         workingDistance=2,
                                         label='XLUMPlanFLN20X',
                                         url="https://www.olympus-lifescience.com/en/objectives/xlumplfln-w/")

class MVPlapo2XC(Objective):
    """ Olympus MVPlapo2XC 0.5 NA with large 
    back aperture.

    """
    def __init__(self):
        super(MVPlapo2XC, self).__init__(f=90/2,
                                         NA=0.5,
                                         focusToFocusLength=137,
                                         backAperture=48,
                                         workingDistance=20,
                                         label='MVPlapo2XC',
                                         url="")

if __name__ == "__main__":
    obj = Objective(f=10, NA=0.8, focusToFocusLength=60, backAperture=18, workingDistance=2, label="Objective")
    print("Focal distances: ", obj.focalDistances())
    print("Position of PP1 and PP2: ", obj.principalPlanePositions(z=0))
    print("Focal spots positions: ", obj.focusPositions(z=0))
    print("Distance between entrance and exit planes: ", obj.L)

    path1 = OpticalPath()
    path1.fanAngle = 0.0
    path1.fanNumber = 1
    path1.rayNumber = 15
    path1.objectHeight = 10.0
    path1.label = "Path with objective"
    path1.append(Space(180))
    path1.append(obj)
    path1.append(Space(10))
    path1.display()

    path2 = OpticalPath()
    path2.fanAngle = 0.0
    path2.fanNumber = 1
    path2.rayNumber = 15
    path2.objectHeight = 10.0
    path2.label = "Path with LUMPLFL40X"
    path2.append(Space(180))
    path2.append(LUMPLFL40X())
    path2.append(Space(10))
    path2.display()

    path3 = OpticalPath()
    path3.fanAngle = 0.0
    path3.fanNumber = 1
    path3.rayNumber = 15
    path3.objectHeight = 10.0
    path3.label = "Path with MVPlapo2XC"
    path3.append(Space(180))
    path3.append(MVPlapo2XC())
    path3.append(Space(10))
    path3.display()
