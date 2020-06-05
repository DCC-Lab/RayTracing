from .matrix import *
from .matrixgroup import *
from math import  *

class System4f(MatrixGroup):
    """
    The matrix group of a 4f system can be defined using this function.

    Parameters
    ----------
    f1 : float
        The focal length of the first lens
    f2 : float
        The focal length of the second lens
    diameter1 : float
        The diameter of the first lens. This value must be positive. (default=+Inf)
    diameter2 : float
        The diameter of the second lens. This value must be positive. (default=+Inf)
    label : string
        The label for the 4f system

    """
    def __init__(self,f1, f2, diameter1=float('+Inf'), diameter2=float('+Inf'), label=''):
        elements = []
        elements.append(Space(d=f1))
        elements.append(Lens(f=f1, diameter=diameter1))
        elements.append(Space(d=f1))
        elements.append(Space(d=f2))
        elements.append(Lens(f=f2, diameter=diameter2))
        elements.append(Space(d=f2))
        super(Telescope, self).__init__(elements=elements, label=label)


class System2f(MatrixGroup):
    """
    The matrix group of a 2f system can be defined using this function.

    Parameters
    ----------
    f : float
        The focal length of the lens
    diameter : float
        The diameter of the lens. This value must be positive. (default=+Inf)
    label : string
        The label for the 2f system

    """
    def __init__(self,f, diameter=float('+Inf'), label=''):
        elements = []
        elements.append(Space(d=f))
        elements.append(Lens(f=f, diameter=diameter))
        elements.append(Space(d=f))
        super(System2f, self).__init__(elements=elements, label=label)

Telescope = System4f

