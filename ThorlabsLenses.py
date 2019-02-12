try:
    from ABCD import *
    from math import  *
    import matplotlib.transforms as transforms

except ImportError:
    raise ImportError('You must have ABCD.py installed. run "python ABCD.py install"')

class ThorlabsAchromatLens(MatrixGroup):
    """ From https://www.thorlabs.com/newgrouppage9.cfm?objectgroup_id=120 

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
        super(ThorlabsAchromatLens, self).__init__(elements=elements)


if __name__ == "__main__":
    fexpected = 50.2
    lens = ThorlabsAchromatLens(fa=fexpected,fb=43.4, R1=33.3,R2=-22.3, R3=-291.1, 
                                tc1=9, tc2=2.5, n1=1.6700, n2=1.7283, diameter=25.4)

    (factual, factual) = lens.focalDistances()
    (p1, p2) = lens.principalPlanePositions(z=0)
    print("actual f = {0:.2f}".format(factual))
    print("expected f = {0:.2f}".format(fexpected))
    print(p1, p2)
