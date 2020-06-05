import unittest
from unittest.mock import patch
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


class TestFigureAxesToDataScale(unittest.TestCase):
    def testWithEmptyImagingPath(self):
        figure = Figure(ImagingPath())

        xScaling, yScaling = figure.axesToDataScale()

        self.assertEqual(xScaling, 1)
        self.assertEqual(yScaling, 1)

    def testWithForcedScale(self):
        figure = Figure(ImagingPath())
        figure.axes.set_xlim(-10, 10)
        figure.axes.set_ylim(-5, 5)

        xScaling, yScaling = figure.axesToDataScale()

        self.assertEqual(xScaling, 20)
        self.assertEqual(yScaling, 10)

    @patch('matplotlib.pyplot.show')
    def testWithImagingPath(self, mock):
        path = ImagingPath()
        path.append(Space(d=10))
        path.append(Lens(f=5))
        path.append(Space(d=10))

        figure = Figure(path)
        figure.display()

        (xScaling, yScaling) = figure.axesToDataScale()

        self.assertEqual(yScaling, figure.displayRange() * 1.5)
        self.assertEqual(xScaling, 20 * 1.1)


if __name__ == '__main__':
    unittest.main()
