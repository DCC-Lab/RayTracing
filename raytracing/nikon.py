from .specialtylenses import *

class LWD16X(Objective):
    """ Nikon 16x immersion objective

    .. csv-table::
        :header: Parameter, value

        "f", "200/16"
        "backAperture", "20"
        "Numerical Aperture (NA)", "1.56"
        "Working Distance (mm)", "3"

    Notes
    -----
    Immersion not considered at this point.
    """

    def __init__(self):
        super(LWD16X, self).__init__(f=200/16,
                                     NA=1.95*0.8,
                                     focusToFocusLength=75,
                                     backAperture=20,
                                     workingDistance=3,
                                     label='CFI75 LWD 16x W',
                                     url="https://www.thorlabs.com/thorproduct.cfm?partnumber=N16XLWD-PF")
