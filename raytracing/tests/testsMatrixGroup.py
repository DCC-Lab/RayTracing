import unittest
from raytracing import *


class TestMatrixGroup(unittest.TestCase):
    def testLargestDiameterWithEmptyGroup(self):
        m = MatrixGroup()
        self.assertEqual(m.largestDiameter(), 0)

    def testLargestDiameterWithFiniteLens(self):
        m = MatrixGroup(elements=[Lens(f=5, diameter=10)])
        self.assertEqual(m.largestDiameter(), 10)
