from .specialtylenses import *

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
                                         label='LUMPlanFL40X',
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
