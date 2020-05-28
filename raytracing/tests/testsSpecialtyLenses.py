import unittest
import envtest # modifies path
import matplotlib.pyplot as plt

from raytracing import *


class TestAchromatDoubletLens(unittest.TestCase):
    @property
    def attributes(self):
        return None

    def setUp(self) -> None:
        self.subclasses = AchromatDoubletLens.__subclasses__()

    def tearDown(self) -> None:
        pass

    def testInit(self):
        for subclass in self.subclasses:
            achromat = subclass()
            self.assertIsNotNone(achromat)
            '''
            for element in achromat.elements:
                attributes = [achromat.fa, achromat.fb, achromat.R1, achromat.R2, achromat.R3, achromat.tc1,
                              achromat.tc2, achromat.te, achromat.n1, achromat.n2, achromat.mat1, achromat.mat2,
                              achromat.url]
                print(attributes)
            '''

    def testDrawAt(self):
        axes = plt.axes()
        for subclass in self.subclasses:
            achromat = subclass()
            achromat.drawAt(1, axes)

    def testDrawAperture(self):
        axes = plt.axes()
        for subclass in self.subclasses:
            achromat = subclass()
            achromat.drawAperture(1, axes)

    def testPointsOfInterest(self):
        for subclass in self.subclasses:
            achromat = subclass()
            poi = achromat.pointsOfInterest(1)


if __name__ == '__main__':
    unittest.main()
