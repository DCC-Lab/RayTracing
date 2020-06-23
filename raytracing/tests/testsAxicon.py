import envtest

from raytracing import *
from numpy import random

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

    def testDeviationAngleIs0(self):
        n = 1
        alpha = random.randint(2000, 5000, 1).item() / 1000
        axicon = Axicon(alpha, n)
        self.assertEqual(axicon.deviationAngle(), 0)

    def testDeviationAngleIs0Too(self):
        n = random.randint(1000, 3000, 1).item() / 1000
        alpha = 0
        axicon = Axicon(alpha, n)
        self.assertEqual(axicon.deviationAngle(), 0)

    def testDeviationAngle(self):
        n = 1.33
        alpha = 4
        axicon = Axicon(alpha, n)
        self.assertAlmostEqual(axicon.deviationAngle(), 1.32, places=15)

    def testFocalLineLengthYIsNoneAndInfiniteDiameter(self):
        n = random.randint(1000, 3000, 1).item() / 1000
        alpha = random.randint(2000, 5000, 1).item() / 1000
        axicon = Axicon(alpha, n)
        self.assertEqual(axicon.focalLineLength(), inf)

    def testFocalLineLengthYIsNone(self):
        n = 1.5
        alpha = 2.6
        axicon = Axicon(alpha, n, 100)
        self.assertAlmostEqual(axicon.focalLineLength(), 38.46153846)

    def testFocalLineLengthNegativeY(self):
        n = 1.43
        alpha = 1.95
        axicon = Axicon(alpha, n, 100)
        self.assertAlmostEqual(axicon.focalLineLength(-2), -2.385211688)

    def testFocalLineLengthPositiveY(self):
        n = 1.43
        alpha = 1.95
        axicon = Axicon(alpha, n, 100)
        self.assertAlmostEqual(axicon.focalLineLength(2), 2.385211688)

    def testMulRayAlreadyBlockedAndYPositive(self):
        ray = Ray(10, -3.141592, isBlocked=True)
        n = 1.1
        alpha = 2.56
        axicon = Axicon(alpha, n, 50)
        outputRay = Ray(10, -3.141592, isBlocked=True)
        # Axicon stuff:
        outputRay.theta -= 0.256
        self.assertEqual(axicon.mul_ray(ray), outputRay)

if __name__ == '__main__':
    envtest.main()