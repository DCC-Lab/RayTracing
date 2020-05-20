import unittest
import envtest  # modifies path
from raytracing import *

class TestMatrixAxesToDataScale(unittest.TestCase):
    def testWithEmptyAxes(self):
        fig, axes = plt.subplots(figsize=(10, 7))

        m = Matrix()

        xScaling, yScaling = m.axesToDataScale(axes)

        self.assertEqual(xScaling, 1)
        self.assertEqual(yScaling, 1)

    def testWithForcedScale(self):
        fig, axes = plt.subplots(figsize=(10, 7))
        axes.set_xlim(-10, 10)
        axes.set_ylim(-5, 5)

        m = Matrix()
        xScaling, yScaling = m.axesToDataScale(axes)

        self.assertEqual(xScaling, 20)
        self.assertEqual(yScaling, 10)

    def testWithEmptyImagingPath(self):
        path = ImagingPath()

        fig, axes = plt.subplots(figsize=(10, 7))
        path.createRayTracePlot(axes=axes)

        (xScaling, yScaling) = path.axesToDataScale(axes)

        self.assertEqual(yScaling, path.displayRange() * 1.5)
        self.assertEqual(xScaling, (2*0.05) * 1.1)  # There's a text for objectHeight displayed at 0.05

    def testWithImagingPath(self):
        """ The test now passes. """
        path = ImagingPath()
        path.append(Space(d=10))
        path.append(Lens(f=5))
        path.append(Space(d=10))

        fig, axes = plt.subplots(figsize=(10, 7))
        path.createRayTracePlot(axes=axes)

        (xScaling, yScaling) = path.axesToDataScale(axes)

        self.assertEqual(yScaling, path.displayRange() * 1.5)
        self.assertEqual(xScaling, 20 * 1.1)


if __name__ == '__main__':
    unittest.main()
