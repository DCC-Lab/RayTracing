from .abcd import *
from math import  *
import matplotlib.transforms as transforms

class EdmundAchromatLens(MatrixGroup):
    """ From https://www.edmundoptics.com/f/VIS-0-Coated-Achromatic-Lenses/13135/

    """

    def __init__(self,fa, fb, R1, R2, R3, tc1, tc2, n1, n2, diameter, label=''):
        self.fa = fa
        self.fb = fb
        self.R1 = R1
        self.R2 = R2
        self.R3 = R3
        self.tc1 = tc1
        self.tc1 = tc2
        self.apertureDiameter = diameter

        elements = []
        elements.append(DielectricInterface(n1=1, n2=n1, R=R1, diameter=diameter))
        elements.append(Space(d=tc1))
        elements.append(DielectricInterface(n1=n1, n2=n2, R=R2, diameter=diameter))
        elements.append(Space(d=tc2))
        elements.append(DielectricInterface(n1=n2, n2=1, R=R3, diameter=diameter))
        super(EdmundAchromatLens, self).__init__(elements=elements)

        # After having built the lens, we confirm that the expected effective
        # focal length (fa) is actually within 1% of the calculated focal length
        (f, f) = self.focalDistances()
        if abs((f-fa)/fa) > 0.01:
            print("Obtained focal distance {0:.4} is not within 1%% of\
                expected {1:.4}".format(f, fa))


class AC75_100(EdmundAchromatLens):
    # Stock number #33-921 
    def __init__(self):
        super(AC75_100,self).__init__(fa=100.00,fb=78.32, R1=64.67,R2=-64.67, R3=-343.59, 
                                    tc1=26.00, tc2=12.7, n1=1.6700, n2=1.8467, diameter=75)

class AC75_200(EdmundAchromatLens):
    # Stock number #88-593  
    def __init__(self):
        super(AC75_200,self).__init__(fa=200.00,fb=187.69, R1=118.81, R2=-96.37, R3=-288.97, 
                                    tc1=17.94, tc2=6.00, n1=1.5168, n2=1.6727, diameter=75)

