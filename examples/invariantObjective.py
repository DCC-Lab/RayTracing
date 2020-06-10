import envexamples

from raytracing import *

"""
DESCRIPTION

Under the objective : NA * FOV = 1 * 1.1 mm = 1.1 mm rad. 
FOV = FN/Mag
At the BA : NA * FOV = 1.1 -> NA = 1.1/FOV = 1.1/22 = 0.05 
"""

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


def opticalPath1(oHeight = None, lensDiameter1 = None, lensDiameter2 = None):

	path = ImagingPath()
	path.objectHeight = oHeight
	path.append(System4f(f1=100, f2=100, diameter1=lensDiameter1, diameter2=lensDiameter2))

	return path

path1 = opticalPath1(oHeight =0.5, lensDiameter1 = 25.4, lensDiameter2 = 25.4)
print(path1.lagrangeInvariant())
path1.display()










