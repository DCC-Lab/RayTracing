import unittest
import envtest  # modifies path
from raytracing import *

inf = float("+inf")


class TestUniformRays(unittest.TestCase):
    def testRays(self):
        rays = UniformRays(1, -1, 1, -1, 10, 11)
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.thetaMax, 1)
        self.assertEqual(rays.thetaMin, -1)
        self.assertEqual(rays.M, 10)
        self.assertEqual(rays.N, 11)

        raysList = []
        for y in linspace(-1, 1, 10):
            for theta in linspace(-1, 1, 11):
                raysList.append(Ray(y, theta))
        self.assertListEqual(rays.rays, raysList)

    def testRaysWithNoneArgs(self):
        rays = UniformRays()
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.thetaMax, pi / 2)
        self.assertEqual(rays.thetaMin, -pi / 2)
        self.assertEqual(rays.M, 100)
        self.assertEqual(rays.N, 100)

        raysList = []
        for y in linspace(-1, 1, 100):
            for theta in linspace(-pi / 2, pi / 2, 100):
                raysList.append(Ray(y, theta))
        self.assertListEqual(rays.rays, raysList)


class TestLambertianRays(unittest.TestCase):

    def testLambertianRays(self):
        rays = LambertianRays(1, -1, 10, 11, 12)
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.M, 10)
        self.assertEqual(rays.N, 11)
        self.assertEqual(rays.I, 12)

        raysList = []
        for theta in linspace(-pi / 2, pi / 2, 11):
            intensity = int(12 * cos(theta))
            for y in linspace(-1, 1, 10):
                for _ in range(intensity):
                    raysList.append(Ray(y, theta))
        self.assertListEqual(rays.rays, raysList)

    def testLambertianRaysNoneArgs(self):
        rays = LambertianRays()
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.M, 100)
        self.assertEqual(rays.N, 100)
        self.assertEqual(rays.I, 100)

        raysList = []
        for theta in linspace(-pi / 2, pi / 2, 100):
            intensity = int(100 * cos(theta))
            for y in linspace(-1, 1, 100):
                for _ in range(intensity):
                    raysList.append(Ray(y, theta))
        self.assertListEqual(rays.rays, raysList)


class TestRandomRays(unittest.TestCase):

    def testRandomRays(self):
        rays = RandomRays()
        self.assertIsNotNone(rays.rays)
        self.assertListEqual(rays.rays, [])

    def testRandomRay(self):
        rays = RandomRays()
        with self.assertRaises(NotImplementedError):
            rays.randomRay()

    def testRandomRayNext(self):
        rays = RandomRays()
        with self.assertRaises(NotImplementedError):
            next(rays)

    def testRandomRaysOutOfBound(self):
        rays = RandomRays(maxCount=1)
        rays.iteration = 1
        with self.assertRaises(StopIteration):
            next(rays)

    def testRandomRaysGetNotOutOfBound(self):
        rays = RandomRays()
        # Test purpose only:
        rays._rays = [Ray()]
        try:
            ray = rays[0]
        except Exception:
            self.fail("This should not raise any exception.")
        self.assertEqual(ray, Ray())

    def testRandomRaysGetButGenerate(self):
        rays = RandomRays()
        with self.assertRaises(UserWarning):
            with warnings.catch_warnings(record=True) as w:
                warnings.simplefilter("error")
                rays[10000]

        with self.assertRaises(NotImplementedError):
            rays[100]

    def testRandomRaysGetOutOfBounds(self):
        rays = RandomRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[item]

    def testRandomRaysGetNegativeIndex(self):
        rays = RandomRays(maxCount=5)
        with self.assertRaises(NotImplementedError):
            rays[-1]

        with self.assertRaises(IndexError):
            rays[-6]


class TestRandomUniformRays(unittest.TestCase):

    def testRandomUniformRays(self):
        rays = RandomUniformRays()
        self.assertIsNotNone(rays.rays)
        self.assertListEqual(rays.rays, [])

    def testRandomUniformRay(self):
        rays = RandomUniformRays(1, 0, pi / 2, 0, maxCount=2)
        randomRay = rays.randomRay()
        self.assertTrue(0 <= randomRay.y <= 1)
        self.assertTrue(0 <= randomRay.theta <= pi / 2)
        self.assertListEqual(rays.rays, [randomRay])

        randomRay2 = rays.randomRay()
        self.assertTrue(0 <= randomRay2.y <= 1)
        self.assertTrue(0 <= randomRay2.theta <= pi / 2)
        self.assertListEqual(rays.rays, [randomRay, randomRay2])

        with self.assertRaises(AttributeError):
            rays.randomRay()

    def testRandomUniformRaysGet(self):
        rays = RandomUniformRays(maxCount=10)
        ray1 = rays.randomRay()

        self.assertEqual(rays[0], ray1)
        self.assertEqual(rays[-10], ray1)

    def testRandomUniformRaysGetGenerate(self):
        rays = RandomUniformRays()

        ray1 = rays[0]
        self.assertListEqual(rays.rays, [ray1])

        ray2 = rays[1000]
        self.assertEqual(len(rays.rays), 1001)
        self.assertEqual(rays.rays[0], ray1)
        self.assertEqual(rays.rays[1000], ray2)

    def testRandomUniformRaysGetGenerateAll(self):
        rays = RandomUniformRays(1, -1, pi / 2, -pi / 2)
        for i in range(len(rays)):
            ray = rays[i]
            self.assertTrue(-1 <= ray.y <= 1)
            self.assertTrue(-pi / 2 <= ray.theta <= pi / 2)

        self.assertEqual(len(rays.rays), len(rays))

    def testRandomUniformRaysNext(self):
        rays = RandomUniformRays(1, -1, pi / 2, -pi / 2)
        ray1 = rays.randomRay()
        nextRay = next(rays)
        self.assertEqual(ray1, nextRay)
        self.assertEqual(len(rays.rays), 1)

        nextRay2 = next(rays)
        self.assertListEqual(rays.rays, [nextRay, nextRay2])

    def testRandomUniformRaysGenerateWithIterations(self):
        rays = RandomUniformRays(10, -10, -1, 1)
        allRays = []
        for ray in rays:
            self.assertTrue(-10 <= ray.y <= 10)
            self.assertTrue(-1 <= ray.theta <= 1)
            allRays.append(ray)

        self.assertEqual(len(rays.rays), len(rays))
        self.assertListEqual(allRays, rays.rays)

    def testRandomUniformRaysGetOutOfBounds(self):
        rays = RandomUniformRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[item]

        with self.assertRaises(IndexError):
            rays[-item]


class TestRandomLambertianRays(unittest.TestCase):

    def testRandomLambertianRays(self):
        rays = RandomLambertianRays()
        self.assertIsNotNone(rays.rays)
        self.assertListEqual(rays.rays, [])

    def testRandomLambertianRay(self):
        rays = RandomLambertianRays(1, 0, maxCount=2)
        randomRay = rays.randomRay()
        self.assertTrue(0 <= randomRay.y <= 1)
        self.assertListEqual(rays.rays, [randomRay])

        randomRay2 = rays.randomRay()
        self.assertTrue(0 <= randomRay2.y <= 1)
        self.assertListEqual(rays.rays, [randomRay, randomRay2])

        with self.assertRaises(AttributeError):
            rays.randomRay()

    def testRandomLambertianRaysGet(self):
        rays = RandomLambertianRays(maxCount=10)
        ray1 = rays.randomRay()

        self.assertEqual(rays[0], ray1)
        self.assertEqual(rays[-10], ray1)

    def testRandomLambertianRaysGetGenerate(self):
        rays = RandomLambertianRays()

        ray1 = rays[0]
        self.assertListEqual(rays.rays, [ray1])

        ray2 = rays[1000]
        self.assertEqual(len(rays.rays), 1001)
        self.assertEqual(rays.rays[0], ray1)
        self.assertEqual(rays.rays[1000], ray2)

    def testRandomLambertianRaysGetGenerateAll(self):
        rays = RandomLambertianRays(1, -1)
        for i in range(len(rays)):
            ray = rays[i]
            self.assertTrue(-1 <= ray.y <= 1)

        self.assertEqual(len(rays.rays), len(rays))

    def testRandomLambertianRaysNext(self):
        rays = RandomLambertianRays(1)
        ray1 = rays.randomRay()
        nextRay = next(rays)
        self.assertEqual(ray1, nextRay)
        self.assertEqual(len(rays.rays), 1)

        nextRay2 = next(rays)
        self.assertListEqual(rays.rays, [nextRay, nextRay2])

    def testRandomLambertianRaysGenerateWithIterations(self):
        rays = RandomLambertianRays(10, -10)
        allRays = []
        for ray in rays:
            self.assertTrue(-10 <= ray.y <= 10)
            allRays.append(ray)

        self.assertEqual(len(rays.rays), len(rays))
        self.assertListEqual(allRays, rays.rays)

    def testRandomLambertianRaysGetOutOfBounds(self):
        rays = RandomLambertianRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[item]

        with self.assertRaises(IndexError):
            rays[-item]


if __name__ == '__main__':
    unittest.main()
