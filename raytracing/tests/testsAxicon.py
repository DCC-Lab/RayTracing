import envtest

from raytracing import *

inf = float("+inf")

class TestAxicon(envtest.RaytracingTestCase):

    def testAxicon(self):
        n = 1.5
        alpha = 2.6
        diameter = 100
        label = "Axicon"
        axicon = Axicon(alpha, n, diameter, label)
        self.assertEqual(axicon.n, n)
        self.assertEqual(axicon.alpha, alpha)
        self.assertEqual(axicon.apertureDiameter, diameter)
        self.assertEqual(axicon.label, label)
        self.assertEqual(axicon.frontIndex, n)
        self.assertEqual(axicon.backIndex, n)
