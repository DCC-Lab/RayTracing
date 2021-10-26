import envtest  # modifies path
from raytracing import *
import numpy as np

inf = float("+inf")


class TestUniformRays(envtest.RaytracingTestCase):
    def testRays(self):
        rays = UniformRays(1, -1, 1, -1, 10, 11)
        raysList = []
        for y in np.linspace(-1, 1, 10):
            for theta in np.linspace(-1, 1, 11):
                raysList.append(Ray(y, theta))
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.thetaMax, 1)
        self.assertEqual(rays.thetaMin, -1)
        self.assertEqual(rays.M, 10)
        self.assertEqual(rays.N, 11)
        self.assertListEqual(rays.rays, raysList)

    def testRaysWithNoneArgs(self):
        rays = UniformRays()
        raysList = []
        for y in np.linspace(-1, 1, 100):
            for theta in np.linspace(-pi / 2, pi / 2, 100):
                raysList.append(Ray(y, theta))
        self.assertIsNotNone(rays)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.thetaMax, pi / 2)
        self.assertEqual(rays.thetaMin, -pi / 2)
        self.assertEqual(rays.M, 100)
        self.assertEqual(rays.N, 100)
        self.assertListEqual(rays.rays, raysList)


class TestLambertianRays(envtest.RaytracingTestCase):

    def testLambertianRays(self):
        rays = LambertianRays(1, -1, 10, 11, 12)
        # raysList = []
        # for theta in np.linspace(-pi / 2, pi / 2, 11):
        #     intensity = int(12 * cos(theta))
        #     for y in np.linspace(-1, 1, 10):
        #         for _ in range(intensity):
        #             raysList.append(Ray(y, theta))
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.M, 10)
        self.assertEqual(rays.N, 11)
        self.assertEqual(rays.I, 12)
        # self.assertListEqual(rays.rays, raysList)

    def testLambertianRaysNoneArgs(self):
        rays = LambertianRays()
        # raysList = []
        # for theta in np.linspace(-pi / 2, pi / 2, 100):
        #     intensity = int(100 * cos(theta))
        #     for y in np.linspace(-1, 1, 100):
        #         for _ in range(intensity):
        #             raysList.append(Ray(y, theta))
        self.assertEqual(rays.yMin, -1)
        self.assertEqual(rays.yMax, 1)
        self.assertEqual(rays.M, 100)
        self.assertEqual(rays.N, 100)
        self.assertEqual(rays.I, 100)
        # self.assertListEqual(rays.rays, raysList)


class TestRandomRays(envtest.RaytracingTestCase):

    def testRandomRays(self):
        rays = RandomRays(maxCount=0)
        self.assertIsNotNone(rays)
        self.assertListEqual(list(rays), [])

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

    def testRandomRaysGetWarnsWhenGeneratingRaysOnlyForLongTimes(self):
        rays = RandomUniformRays(maxCount=1_000_000)
        with self.assertWarns(UserWarning):
            rays[1_000_000-1]

    def testRandomRaysGetNotImplemented(self):
        rays = RandomRays()
        with self.assertRaises(NotImplementedError):
            rays[100]

    def testRandomRaysGetOutOfBounds(self):
        rays = RandomRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[item]

    def testRandomRaysGetNegativeIndexNotImplemented(self):
        rays = RandomRays(maxCount=5)
        with self.assertRaises(NotImplementedError):
            rays[-1]

    def testRandomRaysGetNegativeIndexOutOfBounds(self):
        rays = RandomRays(maxCount=5)
        with self.assertRaises(IndexError):
            rays[-6]


class TestRandomUniformRays(envtest.RaytracingTestCase):

    def testRandomUniformRays(self):
        rays = RandomUniformRays()
        self.assertIsNotNone(rays)

    def testRandomUniformRayRandomRay(self):
        rays = RandomUniformRays(1, 0, pi / 2, 0, maxCount=2)
        randomRay = rays.randomRay()
        randomRay2 = rays.randomRay()
        self.assertTrue(0 <= randomRay.y <= 1)
        self.assertTrue(0 <= randomRay.theta <= pi / 2)
        self.assertTrue(0 <= randomRay2.y <= 1)
        self.assertTrue(0 <= randomRay2.theta <= pi / 2)
        self.assertListEqual([rays[0], rays[1]], [randomRay, randomRay2])

    def testRandomUniformRayRandomRayOutOfBounds(self):
        rays = RandomUniformRays(1, 0, pi / 2, 0, maxCount=2)
        rays.randomRay()
        rays.randomRay()
        with self.assertRaises(AttributeError):
            rays.randomRay()

    def testRandomUniformRaysGet(self):
        rays = RandomUniformRays(maxCount=10)
        ray1 = rays.randomRay()

        self.assertEqual(rays[0], ray1)
        self.assertEqual(rays[-10], ray1)

    def testRandomUniformRaysGetGenerateTheFirst(self):
        rays = RandomUniformRays()
        ray1 = rays[0]

    def testRandomUniformRaysGetGenerateALot(self):
        rays = RandomUniformRays(maxCount=1001)
        ray1 = rays[0]
        ray2 = rays[1000]
        self.assertEqual(len(rays), 1001)
        self.assertEqual(rays[0], ray1)
        self.assertEqual(rays[1000], ray2)

    def testRandomUniformRaysGetGenerateAll(self):
        rays = RandomUniformRays(1, -1, pi / 2, -pi / 2, maxCount=10)
        for i in range(len(rays)):
            ray = rays[i]
            self.assertTrue(-1 <= ray.y <= 1)
            self.assertTrue(-pi / 2 <= ray.theta <= pi / 2)

        self.assertEqual(len(rays.rays), len(rays))

    def testRandomUniformRaysNextFirst(self):
        rays = RandomUniformRays(1, -1, pi / 2, -pi / 2, maxCount=10)
        ray1 = rays.randomRay()
        nextRay = next(rays)
        self.assertEqual(ray1, nextRay)
        self.assertEqual(len(rays), 10)

    def testRandomUniformRaysNextSecond(self):
        rays = RandomUniformRays(1, -1, pi / 2, -pi / 2)
        nextRay = next(rays)
        nextRay2 = next(rays)
        self.assertListEqual([rays[0], rays[1]], [nextRay, nextRay2])

    def testRandomUniformRaysGenerateWithIterations(self):
        rays = RandomUniformRays(10, -10, -1, 1)
        allRays = []
        for ray in rays:
            self.assertTrue(-10 <= ray.y <= 10)
            self.assertTrue(-1 <= ray.theta <= 1)
            allRays.append(ray)

        self.assertEqual(len(rays.rays), len(rays))
        for i in range(len(rays)):
            self.assertEqual(allRays[i], rays[i])

    def testRandomUniformRaysGetOutOfBoundsPositive(self):
        rays = RandomUniformRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[item]

    def testRandomUniformRaysGetOutOfBoundsNegative(self):
        rays = RandomUniformRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[-item]


class TestRandomLambertianRays(envtest.RaytracingTestCase):

    def testRandomLambertianRays(self):
        rays = RandomLambertianRays(maxCount=10)
        self.assertEqual(len(rays), 10)

    def testRandomLambertianRayRandomRay(self):
        rays = RandomLambertianRays(1, 0, maxCount=2)
        randomRay = rays.randomRay()
        randomRay2 = rays.randomRay()
        self.assertTrue(0 <= randomRay.y <= 1)
        self.assertTrue(0 <= randomRay2.y <= 1)
        self.assertEqual(rays[0], randomRay)
        self.assertEqual(rays[1], randomRay2)

    def testRandomLambertianRayRandomRayOutOfBounds(self):
        rays = RandomLambertianRays(1, 0, maxCount=2)
        rays.randomRay()
        rays.randomRay()
        with self.assertRaises(AttributeError):
            rays.randomRay()

    def testRandomLambertianRaysGet(self):
        rays = RandomLambertianRays(maxCount=10)
        ray1 = rays.randomRay()

        self.assertEqual(rays[0], ray1)
        self.assertEqual(rays[-10], ray1)

    def testRandomLambertianRaysGetGeneratALot(self):
        rays = RandomLambertianRays(maxCount=1001)

        ray1 = rays[0]
        ray2 = rays[1000]
        self.assertEqual(len(rays), 1001)
        self.assertEqual(rays[0], ray1)
        self.assertEqual(rays[1000], ray2)

    def testRandomLambertianRaysNextFirst(self):
        rays = RandomLambertianRays(1)
        ray1 = rays.randomRay()
        nextRay = next(rays)
        self.assertEqual(ray1, nextRay)

    def testRandomLambertianRaysNextSecond(self):
        rays = RandomLambertianRays(1)
        nextRay = next(rays)
        nextRay2 = next(rays)
        self.assertListEqual([rays[0], rays[1]], [nextRay, nextRay2])

    def testRandomLambertianRaysGenerateWithIterations(self):
        rays = RandomLambertianRays(10, -10)
        allRays = []
        for ray in rays:
            self.assertTrue(-10 <= ray.y <= 10)
            allRays.append(ray)

        self.assertEqual(len(rays.rays), len(rays))

        for i in range(len(allRays)):
            self.assertEqual(allRays[i], rays[i])

    def testRandomLambertianRaysGetOutOfBoundsPositive(self):
        rays = RandomLambertianRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[item]

    def testRandomLambertianRaysGetOutOfBoundsNegative(self):
        rays = RandomLambertianRays()
        item = int(1e10)
        with self.assertRaises(IndexError):
            rays[-item]


if __name__ == '__main__':
    envtest.main()
