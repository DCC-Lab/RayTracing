import unittest
from unittest.mock import patch
import envtest  # modifies path
from raytracing import *


class TestFigure(unittest.TestCase):
    @patch('raytracing.Figure._showPlot')
    def testDisplayRangeWithFiniteLens(self, mock):
        path = ImagingPath()  # default objectHeight is 10
        path.append(Space(d=10))
        path.append(Lens(f=5, diameter=20))
        path.display()

        largestDiameter = 20

        self.assertEqual(path.figure.displayRange(), largestDiameter)

    @patch('raytracing.Figure._showPlot')
    def testDisplayRangeImageOutOfView(self, mock):
        path = ImagingPath()
        path.append(Space(2))
        path.append(CurvedMirror(-5, 10))
        path.display()

        self.assertAlmostEqual(path.figure.displayRange(), 10)

        path.objectHeight = 1
        path.display()
        self.assertEqual(path.figure.displayRange(), 10)

    def testDisplayRangeWithEmptyPath(self):
        path = ImagingPath()

        largestDiameter = path.objectHeight

        self.assertEqual(path.figure.displayRange(), largestDiameter)

    def testRearrangeRayTraceForPlottingAllNonBlocked(self):
        path = ImagingPath([Space(10), Lens(5, 20), Space(10)])
        initialRay = Ray(0, 1)  # Will go through without being blocked
        listOfRays = path.trace(initialRay)

        xy = path.figure.rearrangeRayTraceForPlotting(listOfRays, True)
        x = [0, 0, 10, 10, 10, 0]
        z = [0, 0, 10, 10, 10, 20]

        self.assertTupleEqual(xy, (z, x))

    def testRearrangeRayTraceForPlottingAllBlockedAndRemoved(self):
        path = ImagingPath([Space(10), Lens(5, 20), Space(10)])
        initialRay = Ray(0, 1.01)  # Will be blocked
        listOfRays = path.trace(initialRay)

        xy = path.figure.rearrangeRayTraceForPlotting(listOfRays, True)

        self.assertTupleEqual(xy, ([], []))

    def testRearrangeRayTraceForPlottingSomeBlockedAndRemoved(self):
        path = ImagingPath([Space(10), Lens(5, 20), Space(10)])
        initialRay = Ray(0, 1.01)  # Will be blocked
        listOfRays = path.trace(initialRay)

        xy = path.figure.rearrangeRayTraceForPlotting(listOfRays, False)
        x = [0, 0, 10.1]
        z = [0, 0, 10]

        self.assertTupleEqual(xy, (z, x))


class TestFigureAxesToDataScale(unittest.TestCase):
    def testWithEmptyImagingPath(self):
        figure = Figure(ImagingPath())
        figure.createFigure()

        xScaling, yScaling = figure.axesToDataScale()

        self.assertEqual(xScaling, 0)
        self.assertEqual(yScaling, 10 * 1.6)

    @unittest.skipIf(sys.platform == 'darwin',"FIXME: We hacked plt.show() on darwin to recover Ctrl-C")
    @patch('matplotlib.pyplot.show')
    def testWithImagingPath(self, mock):
        path = ImagingPath()
        path.append(Space(d=10))
        path.append(Lens(f=5))
        path.append(Space(d=10))

        path.display()

        (xScaling, yScaling) = path.figure.axesToDataScale()

        self.assertEqual(yScaling, path.figure.displayRange() * 1.6)
        self.assertEqual(xScaling, 20 * 1.1)


if __name__ == '__main__':
    unittest.main()
