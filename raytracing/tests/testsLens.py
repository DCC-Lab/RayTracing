import unittest
import envtest # modifies path
from raytracing import *

inf = float("+inf")


class TestLens(unittest.TestCase):
    def testObjectiveCreation(self):
        obj = Objective(f=5, NA=1.0, focusToFocusLength = 10, backAperture=10,workingDistance=1)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.f, 5)
        self.assertEqual(obj.NA, 1.0)
        self.assertEqual(obj.backAperture, 10)
        self.assertEqual(obj.frontAperture, 2)

    def testRaysThroughObjective(self):
        obj = Objective(f=5, NA=1.0, focusToFocusLength = 10, backAperture=10,workingDistance=1)
        self.assertIsNotNone(obj)

        ray = Ray(y=0, theta=0)
        self.assertTrue(obj.traceThrough(ray).isNotBlocked)

        ray = Ray(y=obj.backAperture/2, theta=0)
        self.assertTrue(obj.traceThrough(ray).isNotBlocked)
        self.assertAlmostEqual( abs(obj.traceThrough(ray).theta), obj.NA, 4)

        ray = Ray(y=obj.backAperture/2 * 1.01, theta=0)
        self.assertTrue(obj.traceThrough(ray).isBlocked)

        ray = Ray(y=obj.backAperture, theta=0)
        self.assertTrue(obj.traceThrough(ray).isBlocked)

    def testRaysMultiplicationWithObjective(self):
        # This does not consider apertures except the back aperture
        obj = Objective(f=5, NA=1.0, focusToFocusLength = 10, backAperture=10,workingDistance=1)
        self.assertIsNotNone(obj)

        ray = Ray(y=0, theta=0)
        self.assertTrue( (obj*ray).isNotBlocked)

        ray = Ray(y=obj.backAperture/2, theta=0)
        self.assertTrue((obj*ray).isNotBlocked)
        self.assertAlmostEqual( abs((obj*ray).theta), obj.NA, 4)

        ray = Ray(y=obj.backAperture/2 * 1.01, theta=0)
        self.assertTrue((obj*ray).isBlocked)

        ray = Ray(y=obj.backAperture, theta=0)
        self.assertTrue((obj*ray).isBlocked)


    def testRaysThroughAperture(self):
        aperture = Aperture(diameter=10)
        self.assertIsNotNone(aperture)

        ray = Ray(y=0, theta=0)
        self.assertTrue(aperture.traceThrough(ray).isNotBlocked)

        ray = Ray(y=4.9, theta=0)
        self.assertTrue(aperture.traceThrough(ray).isNotBlocked)

        ray = Ray(y=5.1, theta=0)
        self.assertTrue(aperture.traceThrough(ray).isBlocked)

        ray = Ray(y=9.9, theta=0)
        self.assertTrue(aperture.traceThrough(ray).isBlocked)


    def testOlympus20XObjective(self):
        obj = olympus.XLUMPlanFLN20X()
        self.assertIsNotNone(obj)
        self.assertEqual(obj.backAperture, 22)

    def testOlympus20XObjective(self):
        path = ImagingPath()
        path.append(Space(d=1000))
        obj = olympus.XLUMPlanFLN20X()
        path.append(obj)
        self.assertIsNotNone(obj)
        self.assertEqual(obj.backAperture, 22)
        # print(path.fieldOfView())
        # print(path.imageSize())

    def deactivated_testFlippedOlympus20XObjective(self):
        path = ImagingPath()
        obj = olympus.XLUMPlanFLN20X()
        obj.flipOrientation()
        path.append(obj)
        path.append(Space(d=100))
        self.assertIsNotNone(obj)
        self.assertEqual(obj.backAperture, 22)
        # print(path.fieldOfView())
        # print(path.imageSize())

if __name__ == '__main__':
    unittest.main()
