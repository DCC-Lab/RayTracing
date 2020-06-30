from .specialtylenses import *

class LUMPlanFL40X(Objective):
    """ Olympus 40x immersion objective

    .. csv-table::
        :header: Parameter, value

        "Magnification", "40x"
        "focusToFocusLength", "40"
        "backAperture", "7"
        "Numerical Aperture (NA)", "0.80"
        "Cover Glass Thickness (mm):", "0.00"
        "Diameter (mm)", "21.00"
        "Field Number (mm)", "26.5"
        "Length (mm)", "41.70"
        "Working Distance (mm)", "2"

    Notes
    -----
    Immersion not considered at this point.
    More info: https://www.edmundoptics.com/p/olympus-lumplfln-40xw-objective/3901/
    """

    def __init__(self):
        super(LUMPlanFL40X, self).__init__(f=180/40,
                                         NA=0.8,
                                         focusToFocusLength=40,
                                         backAperture=7,
                                         workingDistance=2,
                                         magnification=40,
                                         fieldNumber=26.5,
                                         label='LUMPlanFL40X',
                                         url="https://www.edmundoptics.com/p/olympus-lumplfln-40xw-objective/3901/")

class XLUMPlanFLN20X(Objective):
    """ Olympus XLUMPlanFLN20X (Super 20X) 1.0 NA with large 
    back aperture.

    .. csv-table::
        :header: Parameter, value

        "Magnification", "20x"
        "focusToFocusLength", "80"
        "backAperture", "22"
        "Numerical Aperture (NA)", "1.00"
        "Cover Glass Thickness (mm)", "0.00"
        "Working Distance (mm)", "2"
        "Objective Field Number (mm)", "22"

    Notes
    -----
    Immersion not considered at this point.
    More info: https://www.olympus-lifescience.com/en/objectives/xlumplfln-w/
    """
    def __init__(self):
        super(XLUMPlanFLN20X, self).__init__(f=180/20,
                                         NA=1.0,
                                         focusToFocusLength=80,
                                         backAperture=22,
                                         workingDistance=2,
                                         magnification=20,
                                         fieldNumber=22,
                                         label='XLUMPlanFLN20X',
                                         url="https://www.olympus-lifescience.com/en/objectives/xlumplfln-w/")

class MVPlapo2XC(Objective):
    """ Olympus MVPlapo2XC 0.5 NA with large 
    back aperture.

    .. csv-table::
        :header: Parameter, value

        "focusToFocusLength", "137"
        "backAperture", "45"
        "Numerical Aperture (NA)", "0.50"
        "Cover Glass Thickness (mm)", "0.00"
        "Working Distance (mm)", "20"


    Notes
    -----
    Immersion not considered at this point.


    """
    def __init__(self):
        super(MVPlapo2XC, self).__init__(f=90/2,
                                         NA=0.5,
                                         focusToFocusLength=137,
                                         backAperture=45,
                                         workingDistance=20,
                                         magnification=2,
                                         fieldNumber=17.6,
                                         label='MVPlapo2XC',
                                         url="")

class UMPLFN20XW(Objective):
    """ Olympus UMPLanFN 20XW immersion objective

    Immersion not considered at this point.

    .. csv-table::
        :header: Parameter, value

        "Magnification", "20x"
        "focusToFocusLength", "45"
        "backAperture", "9"
        "Numerical Aperture (NA)", "0.50"
        "Working Distance (mm)", "3.5"


    Notes
    -----
    Immersion not considered at this point.
    More info: https://www.olympus-lifescience.com/en/objectives/lumplfln-w/#!cms[tab]=%2Fobjectives%2Flumplfln-w%2F20xw

    """
    def __init__(self):
        super(UMPLFN20XW, self).__init__(f=180 / 20,
                                         NA=0.5,
                                         focusToFocusLength=45,
                                         backAperture=9,
                                         workingDistance=3.5,
                                         magnification=20,
                                         fieldNumber=26.5,
                                         label='UMPLFN20XW',
                                         url="https://www.olympus-lifescience.com/en/objectives/lumplfln-w/#!cms[tab]=%"
                                                 "2Fobjectives%2Flumplfln-w%2F20xw")


class XLPLN25X(Objective):
    """ Olympus XLPLN25X 1.05 NA

    .. csv-table::
        :header: Parameter, value

        "Magnification", "25x"
        "focusToFocusLength", "75"
        "backAperture", "18"
        "Numerical Aperture (NA)", "1.05"
        "Working Distance (mm)", "2"


    Notes
    -----
    Immersion not considered at this point.
    More info: https://www.olympus-lifescience.com/en/objectives/multiphoton/

    """

    def __init__(self):
        super(XLPLN25X, self).__init__(f=180/25,
                                         NA=1.05,
                                         focusToFocusLength=75,
                                         backAperture=18,
                                         workingDistance=2,
                                         magnification=25,
                                         fieldNumber=18,
                                         label='XLPLN25X',
                                         url="https://www.olympus-lifescience.com/en/objectives/multiphoton/")
