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

    The complete prescription of all lenses is actually described in a patent:
    https://patents.google.com/patent/US6501603B2/en

    .. csv-table::
        :header: #,   R,   D,   Nd,  υd

         1,  −4.8742, 4.8257, 1.75500, 52.32
         2, −5.4698,  0.2000, , 
         3, −8.2501,  3.5000, 1.56907, 71.30
         4,  −6.7964, 0.1500, , 
         5,  14.8325, 4.6500,  1.43875, 94.99
         6,  −11.8551,1.4000,  1.75500, 52.32
         7,  16.0509, 5.1500,  1.43875, 94.99
         8,  −16.7495,0.2000, , 
         9,  16.6372, 4.2443,  1.56907, 71.30
        10,  −65.8633,0.2000, , 
        11,  12.4106, 5.1500,  1.49700, 81.14
        12,  −46.1798,1.3800,  1.52944, 51.72
        13,  6.3567,  6.4169, , 
        14,  −11.5515,1.2500,  1.52944, 51.72
        15,  10.5297, 5.6154,  1.49700, 81.14
        16,  −15.2713,      0.2000, , 
        17,  −117.7917,   4.0077,  1.56907, 71.30
        18,  −33.7967,    0.1500, , 
        19,  10.0545, 5.2930,  1.49700, 81.14
        20,  −15.1795,    1.3000,  1.52130, 52.55
        21,  8.0217,  7.7007, , 
        22,  −9.5247, 4.2061,  1.58313, 59.38
        23,  −275.8289,   4.3000,  1.59551, 39.29
        24,  −12.9456, , ,

    β = −20X,    NA = 0.8,    F = 9 mm,    WD = 1.4 mm

    - Condition (1) value:    D/F =   8.099
    - Condition (4) value:    | υdpe − υdne | =   20.09
    - Condition (5) value:    | υdpi − υdni | =   28.59 − 29.42
    - Condition (6) value:    rn/rp   =   0.891
    - Condition (7) value:    F/Fg2a  =   −0.311
    - Condition (8) value:    F/Fg2c  =   −0.02

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
