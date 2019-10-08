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
                                         backAperture=45,
                                         workingDistance=20,
                                         label='MVPlapo2XC',
                                         url="")

class UMPLFN20XW(Objective):
    """ Olympus UMPLanFN 20XW immersion objective

    Immersion not considered at this point.

    """
    def __init__(self):
        super(UMPLFN20XW, self).__init__(f=180 / 20,
                                         NA=0.5,
                                         focusToFocusLength=45,
                                         backAperture=9,
                                         workingDistance=3.5,
                                         label='UMPLFN20XW',
                                         url="https://www.olympus-lifescience.com/en/objectives/lumplfln-w/#!cms[tab]=%"
                                                 "2Fobjectives%2Flumplfln-w%2F20xw")


class XLPLN25X(Objective):
    """ Olympus XLPLN25X 1.05 NA

    Immersion not consided at this point
    """

    def __init__(self):
        super(XLPLN25X, self).__init__(f=180/25,
                                         NA=1.05,
                                         focusToFocusLength=75,
                                         backAperture=18,
                                         workingDistance=2,
                                         label='XLPLN25X',
                                         url="https://www.olympus-lifescience.com/en/objectives/multiphoton/")
