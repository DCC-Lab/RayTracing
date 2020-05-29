import unittest
import envtest # modifies path
import matplotlib.pyplot as plt

from raytracing import *


class TestAchromatDoubletLens(unittest.TestCase):
    def testInit(self):
        pass


class TestAchromatDoubletLensSubclasses(unittest.TestCase):
    def setUp(self) -> None:
        self.subclasses = AchromatDoubletLens.__subclasses__()

    def testSubclassesInit(self):
        fails = []
        for subclass in self.subclasses:
            achromat = subclass()

            try:
                self.assertIsNotNone(achromat)
            except AssertionError:
                fails.append('{} not properly initiated.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterest(self):
        fails = []
        z = 0
        for subclass in self.subclasses:
            achromat = subclass()
            points = achromat.pointsOfInterest(z)

            f = -1.0 / achromat.C
            p1 = z - (1 - achromat.D) / achromat.C
            ff = p1 - f

            p2 = z + achromat.L + (1 - achromat.A) / achromat.C
            fb = p2 + f

            try:
                self.assertAlmostEqual(points[0]['z'], ff)
                self.assertAlmostEqual(points[1]['z'], fb)
            except AssertionError:
                fails.append('{} has the wrong points of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)


class TestObjectives(unittest.TestCase):
    def testInit(self):
        pass


class TestObjectivesSubclasses(unittest.TestCase):
    def setUp(self) -> None:
        self.subclasses = Objective.__subclasses__()

    def testSubclassesInit(self):
        fails = []
        for subclass in self.subclasses:
            objective = subclass()

            try:
                self.assertIsNotNone(objective)
            except AssertionError:
                fails.append('{} not properly initiated.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testFlipOrientation(self):
        fails = []
        for subclass in self.subclasses:
            original = subclass()
            flipped = subclass().flipOrientation()

            try:
                self.assertFalse(original.isFlipped)
                self.assertTrue(flipped.isFlipped)
                self.assertNotEqual(original.frontVertex, flipped.frontVertex)
                self.assertNotEqual(original.backVertex, flipped.backVertex)
            except AssertionError:
                fails.append('{} was not properly flipped.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterest(self):
        fails = []
        z = 10
        for subclass in self.subclasses:
            objective = subclass()
            points = objective.pointsOfInterest(z)
            ff = z + objective.focusToFocusLength
            fb = z

            try:
                self.assertAlmostEqual(points[0]['z'], fb)
                self.assertAlmostEqual(points[1]['z'], ff)
            except AssertionError:
                fails.append('{} has the wrong point of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)

    def testPointsOfInterestFlipped(self):
        fails = []
        z = 10
        for subclass in self.subclasses:
            objective = subclass()
            points = objective.pointsOfInterest(z)
            ff = z + objective.focusToFocusLength
            fb = z

            try:
                self.assertAlmostEqual(points[0]['z'], fb)
                self.assertAlmostEqual(points[1]['z'], ff)
            except AssertionError:
                fails.append('{} has the wrong point of interest.'.format(subclass.__name__))
        self.assertEqual([], fails)


if __name__ == '__main__':
    unittest.main()
