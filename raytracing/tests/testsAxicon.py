import envtest

from raytracing import *
from numpy import random

inf = float("+inf")
degrees = math.pi/180

class TestAxicon(envtest.RaytracingTestCase):

    def testAxicon(self):
        n = 1.5
        alpha = 2.6*degrees
        diameter = 100
        label = "Axicon"
        axicon = Axicon(alpha, n, diameter, label)
        self.assertEqual(axicon.n, n)
        self.assertEqual(axicon.alpha, alpha)
        self.assertEqual(axicon.apertureDiameter, diameter)
        self.assertEqual(axicon.label, label)
        self.assertEqual(axicon.frontIndex, 1.0)
        self.assertEqual(axicon.backIndex, 1.0)

    def testDeviationAngleIs0(self):
        n = 1
        alpha = random.randint(2000, 5000, 1).item() / 1000*degrees
        axicon = Axicon(alpha, n)
        self.assertEqual(axicon.deviationAngle(), 0)

    def testDeviationAngleIs0Too(self):
        n = random.randint(1000, 3000, 1).item() / 1000
        alpha = 0*degrees
        axicon = Axicon(alpha, n)
        self.assertEqual(axicon.deviationAngle(), 0)

    def testDeviationAngle(self):
        n = 1.33
        alpha = 4*degrees
        axicon = Axicon(alpha, n)
        self.assertAlmostEqual(axicon.deviationAngle(), 1.32*degrees, places=15)

    def testFocalLineLengthYIsNoneAndInfiniteDiameter(self):
        n = random.randint(1000, 3000, 1).item() / 1000
        alpha = random.randint(2000, 5000, 1).item() / 1000*degrees
        axicon = Axicon(alpha, n)
        self.assertEqual(axicon.focalLineLength(), inf)

    def testFocalLineLengthYIsNone(self):
        n = 1.5
        alpha = 2.6*degrees
        axicon = Axicon(alpha, n, 100)
        self.assertAlmostEqual(axicon.focalLineLength(), 38.46153846)

    def testFocalLineLengthNegativeY(self):
        n = 1.43
        alpha = 1.95*degrees
        axicon = Axicon(alpha=alpha, n=n, diameter=100)
        self.assertAlmostEqual(axicon.focalLineLength(-2), axicon.focalLineLength(2))

    def testFocalLineLengthPositiveY(self):
        n = 1.43
        alpha = 1.95*degrees
        axicon = Axicon(alpha, n, 100)
        self.assertAlmostEqual(axicon.focalLineLength(2), 2.385211688)

    def testMulRayYPositive(self):
        ray = Ray(10, -3.141592)
        n = 1.1
        alpha = 2.56*degrees
        axicon = Axicon(alpha, n, 50)
        outputRay = Ray(10, -3.141592)
        # Axicon stuff:
        outputRay.theta -= 0.256
        self.assertEqual(axicon.mul_ray(ray), outputRay)

    def testMulRayYNegative(self):
        ray = Ray(-10, 3.141592)
        n = 1.1
        alpha = 2.56*degrees
        axicon = Axicon(alpha, n, 50)
        outputRay = Ray(-10, 3.141592)
        # Axicon stuff:
        outputRay.theta += 0.256
        self.assertEqual(axicon.mul_ray(ray), outputRay)

    def testMulMatrix(self):
        matrix = Matrix()
        axicon = Axicon(2.6543, 1.2*degrees)
        with self.assertRaises(TypeError):
            axicon.mul_matrix(matrix)

    def testDifferentMultiplications(self):
        ray = Ray()
        beam = GaussianBeam(w=1, R=10, n=1.67)
        matrix = Matrix()
        axicon = Axicon(4.3, 1.67*degrees)
        self.assertIsNotNone(axicon * ray)
        with self.assertRaises(TypeError):
            axicon * beam

        with self.assertRaises(TypeError):
            axicon * matrix

if __name__ == '__main__':
    envtest.main()
