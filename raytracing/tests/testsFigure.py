import unittest
import envtest  # modifies path
from raytracing import *


class TestFigure(unittest.TestCase):
    def testDisplayRangeWithFiniteLens(self):
        path = ImagingPath()  # default objectHeight is 10
        path.append(Space(d=10))
        path.append(Lens(f=5, diameter=20))
        figure = Figure(path)

        largestDiameter = 20

        self.assertEqual(figure.displayRange(), largestDiameter)

    def testDisplayRange(self):
        path = ImagingPath()
        path.append(Space(2))
        path.append(CurvedMirror(-5, 10))
        figure = Figure(path)
        self.assertAlmostEqual(figure.displayRange(), 5 * 10)

        path.objectHeight = 1
        self.assertEqual(figure.displayRange(), 10)

    def testDisplayRangeWithEmptyPath(self):
        path = ImagingPath()
        figure = Figure(path)

        largestDiameter = path.objectHeight * 2

        self.assertEqual(figure.displayRange(), largestDiameter)
