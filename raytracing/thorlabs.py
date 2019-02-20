from .abcd import *
from math import  *
import matplotlib.transforms as transforms

class DoubletAchromatLens(MatrixGroup):
    """ Nomenclature from https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120 

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
        super(DoubletAchromatLens, self).__init__(elements=elements)

        # After having built the lens, we confirm that the expected effective
        # focal length (fa) is actually within 1% of the calculated focal length
        (f, f) = self.focalDistances()
        if abs((f-fa)/fa) > 0.01:
            print("Obtained focal distance {0:.4} is not within 1%% of\
                expected {1:.4}".format(f, fa))


class AC254_050_A(DoubletAchromatLens):
    def __init__(self):
        super(AC254_050_A,self).__init__(fa=50.2,fb=43.4, R1=33.3,R2=-22.28, R3=-291.07, 
                                    tc1=9, tc2=2.5, n1=1.6700, n2=1.7283, diameter=25.4)

class AC254_045_A(DoubletAchromatLens):
    def __init__(self):
        super(AC254_045_A,self).__init__(fa=45.0,fb=40.2, R1=31.2, R2=-25.90, R3=-130.6, 
                                    tc1=7, tc2=2.0, n1=1.6700, n2=1.8052, diameter=25.4)

