from .matrix import *
from .matrixgroup import *
from math import  *

class System4f(MatrixGroup):
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
    def __init__(self,f, diameter=float('+Inf'), label=''):
        elements = []
        elements.append(Space(d=f))
        elements.append(Lens(f=f, diameter=diameter))
        elements.append(Space(d=f))
        super(System2f, self).__init__(elements=elements, label=label)

Telescope = System4f

