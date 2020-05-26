import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestUniformRays(unittest.TestCase):

    def testUniformRays(self):
        rays = UniformRays(10, 1, pi / 2, 0, 100, 100)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 10)
        self.assertEqual(rays.yMin, 1)
        self.assertEqual(rays.thetaMax, pi / 2)
        self.assertEqual(rays.thetaMin, 0)
        self.assertEqual(rays.M, 100)
        self.assertEqual(rays.N, 100)
        allY = linspace(1, 10, 100)
        allTheta = linspace(0, pi / 2, 100)
        allRays = []
        for y in allY:
            for theta in allTheta:
                allRays.append(Ray(y, theta))
        self.assertListEqual(rays.rays, allRays)

    def testUniformRaysNoneInArgs(self):
        rays = UniformRays(10, None, pi / 4, None, 50, 54)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 10)
        self.assertEqual(rays.yMin, -10)
        self.assertEqual(rays.thetaMax, pi / 4)
        self.assertEqual(rays.thetaMin, -pi / 4)
        self.assertEqual(rays.M, 50)
        self.assertEqual(rays.N, 54)
        allY = linspace(-10, 10, 50)
        allTheta = linspace(-pi / 4, pi / 4, 54)
        allRays = []
        for y in allY:
            for theta in allTheta:
                allRays.append(Ray(y, theta))
        self.assertListEqual(rays.rays, allRays)


class TestLambertianRays(unittest.TestCase):

    def testLambertianRays(self):
        rays = LambertianRays(10, 0, 10, 10, 10)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 10)
        self.assertEqual(rays.yMin, 0)
        self.assertEqual(rays.thetaMax, pi / 2)
        self.assertEqual(rays.thetaMin, -pi / 2)
        self.assertEqual(rays.M, 10)
        self.assertEqual(rays.N, 10)
        self.assertEqual(rays.I, 10)
        allRays = []
        for theta in linspace(-pi / 2, pi / 2, 10):
            intensity = int(10 * cos(theta))
            for y in linspace(0, 10, 10):
                for _ in range(intensity):
                    allRays.append(Ray(y, theta))
        self.assertListEqual(rays.rays, allRays)

    def testLambertianRaysNoneInArgs(self):
        rays = LambertianRays(10, None, 10, 10, 10)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 10)
        self.assertEqual(rays.yMin, -10)
        self.assertEqual(rays.thetaMax, pi / 2)
        self.assertEqual(rays.thetaMin, -pi / 2)
        self.assertEqual(rays.M, 10)
        self.assertEqual(rays.N, 10)
        self.assertEqual(rays.I, 10)
        allRays = []
        for theta in linspace(-pi / 2, pi / 2, 10):
            intensity = int(10 * cos(theta))
            for y in linspace(-10, 10, 10):
                for _ in range(intensity):
                    allRays.append(Ray(y, theta))
        self.assertListEqual(rays.rays, allRays)


class TestRandomRays(unittest.TestCase):

    def testRandomRays(self):
        rays = RandomRays(10, 0, pi / 3, 0, 100)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.maxCount, 100)
        self.assertEqual(rays.yMax, 10)
        self.assertEqual(rays.yMin, 0)
        self.assertEqual(rays.thetaMax, pi / 3)
        self.assertEqual(rays.thetaMin, 0)

    def testRandomRaysWithNoneInArgs(self):
        rays = RandomRays(10, None, pi / 2, None, 1000)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.maxCount, 1000)
        self.assertEqual(rays.yMax, 10)
        self.assertEqual(rays.yMin, -10)
        self.assertEqual(rays.thetaMax, pi / 2)
        self.assertEqual(rays.thetaMin, -pi / 2)

    def testRandomRay(self):
        rays = RandomRays()
        with self.assertRaises(NotImplementedError):
            rays.randomRay()

    def testLen(self):
        rays = RandomRays(maxCount=10)
        self.assertEqual(len(rays), 10)

    def testNext(self):
        rays = RandomRays()
        with self.assertRaises(NotImplementedError):
            next(rays)

    def testNextOutOfBound(self):
        rays = RandomRays(maxCount=1)
        rays.iteration = 1
        with self.assertRaises(StopIteration):
            next(rays)


if __name__ == '__main__':
    unittest.main()
